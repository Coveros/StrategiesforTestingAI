import logging
import os
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional

import chromadb
import requests
from chromadb.config import Settings
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables from project root for consistent behavior
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Simplified Retrieval-Augmented Generation pipeline using local embeddings,
    Ollama-hosted SLM generation, and ChromaDB.

    This class implements a complete RAG system with some intentional issues
    for students to discover during testing exercises.
    """

    def __init__(self):
        """Initialize the RAG pipeline."""
        self.provider_name = "ollama"
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

        try:
            self.ollama_timeout_seconds = max(15, int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120")))
        except ValueError:
            self.ollama_timeout_seconds = 120

        self.provider_client: bool = False
        self.embedding_client: Optional[SentenceTransformer] = None
        self.vector_db = None
        self.collection = None

        self.stats = {
            "queries_processed": 0,
            "total_response_time": 0,
            "documents_loaded": 0,
            "average_retrieval_time": 0,
            "errors": 0,
        }

        self._initialize_components()

    def _initialize_components(self):
        """Initialize all pipeline components."""
        try:
            self._initialize_embedding_model()
            self._verify_ollama_connection()
            self._initialize_vector_db()
            self._load_documents()
        except Exception as e:
            logger.error("Failed to initialize RAG pipeline: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def _initialize_embedding_model(self):
        """Initialize the local sentence-transformer embedding model."""
        try:
            self.embedding_client = SentenceTransformer(self.embedding_model_name)
            logger.info("Embedding model initialized successfully: %s", self.embedding_model_name)
        except Exception as e:
            raise RuntimeError(
                "Failed to initialize local embedding model. "
                f"EMBEDDING_MODEL={self.embedding_model_name}. Root cause: {e}"
            ) from e

    def _verify_ollama_connection(self):
        """Verify Ollama service availability and record whether model is present."""
        url = f"{self.ollama_host}/api/tags"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            payload = response.json()
            models = payload.get("models", [])
            names = {m.get("name", "") for m in models if isinstance(m, dict)}

            if self.ollama_model in names:
                self.provider_client = True
                logger.info("Ollama model available: %s", self.ollama_model)
            else:
                self.provider_client = False
                logger.warning(
                    "Ollama is reachable but model '%s' is not pulled yet. "
                    "Run: ollama pull %s",
                    self.ollama_model,
                    self.ollama_model,
                )
        except Exception as e:
            raise RuntimeError(
                "Could not connect to Ollama at "
                f"{self.ollama_host}. Ensure Ollama is running and reachable. Root cause: {e}"
            ) from e

    def _initialize_vector_db(self):
        """Initialize ChromaDB vector database."""
        try:
            db_path = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
            os.makedirs(db_path, exist_ok=True)

            try:
                self.vector_db = chromadb.PersistentClient(
                    path=db_path,
                    settings=Settings(anonymized_telemetry=False),
                )
            except BaseException as init_error:
                # Recovery path for local Chroma metadata corruption/version drift.
                error_text = str(init_error)
                recoverable_markers = (
                    "default_tenant",
                    "range start index",
                    "out of range for slice",
                    "PanicException",
                )

                if any(marker in error_text for marker in recoverable_markers):
                    backup_path = f"{db_path}_backup_{int(time.time())}"
                    logger.warning(
                        "Chroma initialization failed with recoverable local-store error (%s); backing up DB to %s and rebuilding.",
                        error_text,
                        backup_path,
                    )
                    try:
                        os.rename(db_path, backup_path)
                    except Exception as rename_error:
                        logger.error("Failed to backup corrupt Chroma directory: %s", rename_error)
                        raise init_error

                    os.makedirs(db_path, exist_ok=True)
                    self.vector_db = chromadb.PersistentClient(
                        path=db_path,
                        settings=Settings(anonymized_telemetry=False),
                    )
                else:
                    raise

            collection_name = os.getenv("VECTOR_COLLECTION", "genai_testing_docs_local_v1")
            try:
                self.collection = self.vector_db.get_collection(collection_name)

                # Test existing collection compatibility with current embedding dimensions.
                try:
                    test_embedding = self._generate_embeddings(["test compatibility"])[0]
                    self.collection.query(query_embeddings=[test_embedding], n_results=1)
                    logger.info("Loaded existing collection: %s", collection_name)
                except Exception as query_error:
                    logger.info("Existing collection incompatible (%s), recreating...", query_error)
                    self.vector_db.delete_collection(collection_name)
                    raise RuntimeError("Need to recreate collection")
            except Exception:
                try:
                    self.collection = self.vector_db.create_collection(
                        name=collection_name,
                        metadata={
                            "hnsw:space": "cosine",
                            "description": "GenAI testing tutorial documents (local embeddings)",
                        },
                    )
                except Exception as create_error:
                    if "already exists" in str(create_error):
                        self.vector_db.delete_collection(collection_name)
                        self.collection = self.vector_db.create_collection(
                            name=collection_name,
                            metadata={
                                "hnsw:space": "cosine",
                                "description": "GenAI testing tutorial documents (local embeddings)",
                            },
                        )
                    else:
                        raise

                logger.info("Created new collection: %s", collection_name)
                self._load_documents()
        except Exception as e:
            logger.error("Failed to initialize vector database: %s", str(e))
            raise

    def _load_documents(self):
        """Load and process documents into the vector database."""
        try:
            docs_path = os.path.join(os.path.dirname(__file__), "..", "data", "documents")

            if not os.path.exists(docs_path):
                logger.warning("Documents directory not found: %s", docs_path)
                return

            existing_count = self.collection.count()
            if existing_count > 0:
                logger.info("Collection already contains %s documents", existing_count)
                self.stats["documents_loaded"] = existing_count
                return

            documents = []
            for filename in os.listdir(docs_path):
                if filename.endswith(".md"):
                    filepath = os.path.join(docs_path, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        documents.append({
                            "content": content,
                            "metadata": {"source": filename},
                        })

            logger.info("Loaded %s documents", len(documents))

            if not documents:
                logger.warning("No documents found to load")
                return

            doc_chunks = []
            for doc in documents:
                chunks = self._split_text(doc["content"])
                for i, chunk in enumerate(chunks):
                    doc_chunks.append({
                        "content": chunk,
                        "metadata": {**doc["metadata"], "chunk_id": i},
                    })

            logger.info("Created %s document chunks", len(doc_chunks))
            self._add_documents_to_db(doc_chunks)

            self.stats["documents_loaded"] = len(doc_chunks)
            logger.info("Document loading completed successfully")
        except Exception as e:
            logger.error("Failed to load documents: %s", str(e))
            logger.error(traceback.format_exc())
            raise

    def _split_text(self, text: str, chunk_size: int = 2000, chunk_overlap: int = 200) -> List[str]:
        """Simple text splitting function."""
        # INTENTIONAL ISSUE: Chunk size too large for optimal retrieval.
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            if end < len(text):
                last_period = text.rfind(".", start, end)
                if last_period > start:
                    end = last_period + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = max(start + chunk_size - chunk_overlap, end)

        return chunks

    def _add_documents_to_db(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector database with local embeddings."""
        try:
            texts = [doc["content"] for doc in documents]
            metadatas = [doc["metadata"] for doc in documents]

            embeddings = self._generate_embeddings(texts)
            ids = [f"doc_{i}" for i in range(len(texts))]

            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids,
            )

            logger.info("Added %s documents to vector database", len(texts))
        except Exception as e:
            logger.error("Failed to add documents to database: %s", str(e))
            raise

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate normalized embeddings for texts using a local model."""
        if not self.embedding_client:
            raise RuntimeError("Embedding model is not initialized")

        try:
            vectors = self.embedding_client.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            return vectors.tolist()
        except Exception as e:
            logger.error("Failed to generate embeddings: %s", str(e))
            raise

    def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a query."""
        embeddings = self._generate_embeddings([query])
        return embeddings[0]

    def _create_smart_preview(self, text: str, max_length: int = 300) -> str:
        """Create a smart preview of text that avoids cutting off mid-word/sentence."""
        if len(text) <= max_length:
            return text

        truncated = text[:max_length]

        for ending in [". ", ".\n", "! ", "!\n", "? ", "?\n"]:
            last_sentence = truncated.rfind(ending)
            if last_sentence > max_length * 0.7:
                return text[: last_sentence + 1] + "..."

        last_space = truncated.rfind(" ")
        if last_space > max_length * 0.8:
            return text[:last_space] + "..."

        return text[: max_length - 3] + "..."

    def _retrieve_documents(self, query: str, n_results: int = None) -> Dict[str, Any]:
        """Retrieve relevant documents for a query."""
        start_time = time.time()

        try:
            if n_results is None:
                n_results = int(os.getenv("MAX_RETRIEVAL_DOCS", "5"))

            query_embedding = self._generate_query_embedding(query)
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"],
            )

            retrieval_time = time.time() - start_time
            self.stats["average_retrieval_time"] = (
                (self.stats["average_retrieval_time"] * self.stats["queries_processed"] + retrieval_time)
                / (self.stats["queries_processed"] + 1)
            )

            return {
                "documents": results["documents"][0] if results["documents"] else [],
                "metadatas": results["metadatas"][0] if results["metadatas"] else [],
                "distances": results["distances"][0] if results["distances"] else [],
                "retrieval_time": retrieval_time,
            }
        except Exception as e:
            logger.error("Failed to retrieve documents: %s", str(e))
            self.stats["errors"] += 1
            raise

    def _generate_response(self, query: str, context_docs: List[str], temperature: Optional[float] = None) -> str:
        """Generate response using an Ollama-hosted SLM with retrieved context."""
        try:
            context = "\n\n".join(context_docs[:3])
            if temperature is None:
                try:
                    default_temp = float(os.getenv("TEMPERATURE", "0.3"))
                except ValueError:
                    default_temp = 0.3
                effective_temperature = min(max(default_temp, 0.0), 1.0)
            else:
                effective_temperature = float(temperature)

            max_tokens_env = os.getenv("MAX_TOKENS", "600")
            try:
                max_tokens = max(64, int(max_tokens_env))
            except ValueError:
                max_tokens = 600

            prompt = (
                "You are a GenAI testing tutor. Use the provided context to answer directly and helpfully. "
                "Do not begin with disclaimers about missing context unless the context is truly empty. "
                "If context is partial, still provide the best concise answer grounded in available context, "
                "then add one short line: 'Additional context that would help: ...'.\n\n"
                f"Question: {query}\n\n"
                f"Context:\n{context}\n\n"
                "Answer with:\n"
                "1) A concise direct answer (4-8 bullets for list-style questions).\n"
                "2) Optional 'Additional context that would help' line only if needed.\n"
                "3) Stay on the asked question; do not add extra sections unless requested.\n"
                "4) No references to internal prompt rules.\n"
                "Answer:"
            )

            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": effective_temperature,
                    # INTENTIONAL ISSUE: Sometimes too short for complete answers.
                    "num_predict": max_tokens,
                },
            }

            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json=payload,
                timeout=self.ollama_timeout_seconds,
            )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Ollama generate failed ({response.status_code}): {response.text[:400]}"
                )

            body = response.json()
            text = (body.get("response") or "").strip()
            if not text:
                raise RuntimeError("Ollama returned an empty response")

            return text
        except Exception as e:
            logger.error("Failed to generate response: %s", str(e))
            self.stats["errors"] += 1
            raise

    def query(self, user_query: str, temperature: Optional[float] = None) -> Dict[str, Any]:
        """Process a user query and return response with metadata."""
        start_time = time.time()

        try:
            if not user_query or not user_query.strip():
                raise ValueError("Empty query provided")

            retrieval_results = self._retrieve_documents(user_query)
            response_text = self._generate_response(
                user_query,
                retrieval_results["documents"],
                temperature=temperature,
            )

            if temperature is None:
                try:
                    default_temp = float(os.getenv("TEMPERATURE", "0.3"))
                except ValueError:
                    default_temp = 0.3
                effective_temperature = min(max(default_temp, 0.0), 1.0)
            else:
                effective_temperature = float(temperature)
            total_time = time.time() - start_time

            self.stats["queries_processed"] += 1
            self.stats["total_response_time"] += total_time

            return {
                "response": response_text,
                "sources": [
                    {
                        "content": self._create_smart_preview(doc),
                        "metadata": meta,
                        "similarity": round(max(0, (1 - dist) * 100), 1),
                    }
                    for doc, meta, dist in zip(
                        retrieval_results["documents"][:3],
                        retrieval_results["metadatas"][:3],
                        retrieval_results["distances"][:3],
                    )
                ],
                "retrieval_time": retrieval_results["retrieval_time"],
                "generation_time": total_time - retrieval_results["retrieval_time"],
                "total_time": total_time,
                "temperature": effective_temperature,
            }
        except Exception as e:
            error_time = time.time() - start_time
            self.stats["errors"] += 1
            logger.error("Query processing failed: %s", str(e))

            return {
                "response": f"I apologize, but I encountered an error processing your query: {str(e)}",
                "sources": [],
                "error": str(e),
                "total_time": error_time,
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics for monitoring."""
        avg_response_time = (
            self.stats["total_response_time"] / self.stats["queries_processed"]
            if self.stats["queries_processed"] > 0
            else 0
        )

        return {
            "queries_processed": self.stats["queries_processed"],
            "average_response_time": round(avg_response_time, 3),
            "average_retrieval_time": round(self.stats["average_retrieval_time"], 3),
            "documents_loaded": self.stats["documents_loaded"],
            "error_count": self.stats["errors"],
            "error_rate": (
                self.stats["errors"] / self.stats["queries_processed"]
                if self.stats["queries_processed"] > 0
                else 0
            ),
            "provider": self.provider_name,
            "model": self.ollama_model,
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of all components."""
        health = {
            "provider": self.provider_name,
            "provider_client": False,
            "vector_db": False,
            "collection": False,
            "documents_loaded": False,
            "ollama_host": self.ollama_host,
            "ollama_model": self.ollama_model,
            # Backward-compatible key expected by existing UI/logic.
            "cohere_client": False,
        }

        try:
            tags_resp = requests.get(f"{self.ollama_host}/api/tags", timeout=10)
            if tags_resp.status_code == 200:
                models = tags_resp.json().get("models", [])
                names = {m.get("name", "") for m in models if isinstance(m, dict)}
                has_model = self.ollama_model in names
                health["provider_client"] = has_model
                health["cohere_client"] = has_model

            if self.vector_db and self.collection:
                health["vector_db"] = True
                health["collection"] = True
                health["documents_loaded"] = self.collection.count() > 0
        except Exception as e:
            logger.error("Health check failed: %s", str(e))

        return health
