import os
import logging
import time
import traceback
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

import cohere
import chromadb
from chromadb.config import Settings

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Simplified Retrieval-Augmented Generation pipeline using Cohere and ChromaDB.
    
    This class implements a complete RAG system with some intentional issues
    for students to discover during testing exercises.
    """
    
    def __init__(self):
        """Initialize the RAG pipeline."""
        self.cohere_client = None
        self.vector_db = None
        self.collection = None
        self.stats = {
            'queries_processed': 0,
            'total_response_time': 0,
            'documents_loaded': 0,
            'average_retrieval_time': 0,
            'errors': 0
        }
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all pipeline components."""
        try:
            # Initialize Cohere client
            api_key = os.getenv('COHERE_API_KEY')
            if not api_key:
                raise ValueError("COHERE_API_KEY environment variable not set")
            
            self.cohere_client = cohere.Client(api_key)
            logger.info("Cohere client initialized successfully")
            
            # Initialize ChromaDB
            self._initialize_vector_db()
            
            # Load documents
            self._load_documents()
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _initialize_vector_db(self):
        """Initialize ChromaDB vector database."""
        try:
            # Create persistent database
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'chroma_db')
            os.makedirs(db_path, exist_ok=True)
            
            self.vector_db = chromadb.PersistentClient(
                path=db_path,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection with cosine similarity
            collection_name = "genai_testing_docs_v3"  # New collection name for v3 embeddings
            try:
                # Try to get existing collection
                self.collection = self.vector_db.get_collection(collection_name)
                
                # Test if the collection works with current embedding model
                try:
                    # Test with actual embedding to catch dimension mismatches
                    test_embedding = self.cohere_client.embed(
                        texts=["test compatibility"],
                        model="embed-english-v3.0",
                        input_type="search_query"
                    ).embeddings[0]
                    
                    # Try a query with the embedding
                    test_query = self.collection.query(
                        query_embeddings=[test_embedding],
                        n_results=1
                    )
                    logger.info(f"Loaded existing collection: {collection_name}")
                except Exception as query_error:
                    # Collection exists but has incompatible embeddings - delete and recreate
                    logger.info(f"Existing collection incompatible ({query_error}), recreating...")
                    self.vector_db.delete_collection(collection_name)
                    raise Exception("Need to recreate collection")
                    
            except Exception:
                # Collection doesn't exist or needs recreation - create with cosine similarity
                try:
                    self.collection = self.vector_db.create_collection(
                        name=collection_name,
                        metadata={"hnsw:space": "cosine", "description": "GenAI testing tutorial documents"}
                    )
                except Exception as create_error:
                    if "already exists" in str(create_error):
                        # Force delete and retry
                        try:
                            self.vector_db.delete_collection(collection_name)
                            self.collection = self.vector_db.create_collection(
                                name=collection_name,
                                metadata={"hnsw:space": "cosine", "description": "GenAI testing tutorial documents"}
                            )
                        except Exception as retry_error:
                            raise Exception(f"Failed to create collection after deletion: {retry_error}")
                    else:
                        raise create_error
                logger.info(f"Created new collection: {collection_name}")
                # Load documents into the new collection
                self._load_documents()
                
        except Exception as e:
            logger.error(f"Failed to initialize vector database: {str(e)}")
            raise
    
    def _load_documents(self):
        """Load and process documents into the vector database."""
        try:
            docs_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'documents')
            
            if not os.path.exists(docs_path):
                logger.warning(f"Documents directory not found: {docs_path}")
                return
            
            # Check if documents are already loaded
            existing_count = self.collection.count()
            if existing_count > 0:
                logger.info(f"Collection already contains {existing_count} documents")
                self.stats['documents_loaded'] = existing_count
                return
            
            # Load documents manually
            documents = []
            for filename in os.listdir(docs_path):
                if filename.endswith('.md'):
                    filepath = os.path.join(docs_path, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            'content': content,
                            'metadata': {'source': filename}
                        })
            
            logger.info(f"Loaded {len(documents)} documents")
            
            if not documents:
                logger.warning("No documents found to load")
                return
            
            # Split documents into chunks
            doc_chunks = []
            for doc in documents:
                chunks = self._split_text(doc['content'])
                for i, chunk in enumerate(chunks):
                    doc_chunks.append({
                        'content': chunk,
                        'metadata': {**doc['metadata'], 'chunk_id': i}
                    })
            
            logger.info(f"Created {len(doc_chunks)} document chunks")
            
            # Process chunks and add to vector database
            self._add_documents_to_db(doc_chunks)
            
            self.stats['documents_loaded'] = len(doc_chunks)
            logger.info("Document loading completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to load documents: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _split_text(self, text: str, chunk_size: int = 2000, chunk_overlap: int = 200) -> List[str]:
        """Simple text splitting function."""
        # INTENTIONAL ISSUE: Chunk size too large for optimal retrieval
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            if end < len(text):
                # Try to split at sentence boundary
                last_period = text.rfind('.', start, end)
                if last_period > start:
                    end = last_period + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = max(start + chunk_size - chunk_overlap, end)
        
        return chunks
    
    def _add_documents_to_db(self, documents: List[Dict]):
        """Add documents to the vector database with embeddings."""
        try:
            texts = [doc['content'] for doc in documents]
            metadatas = [doc['metadata'] for doc in documents]
            
            # Generate embeddings using Cohere
            embeddings = self._generate_embeddings(texts)
            
            # Create IDs for documents
            ids = [f"doc_{i}" for i in range(len(texts))]
            
            # Add to collection
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(texts)} documents to vector database")
            
        except Exception as e:
            logger.error(f"Failed to add documents to database: {str(e)}")
            raise
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts using Cohere."""
        try:
            # Using embed-english-v3.0 for consistent 1024-dimensional embeddings
            response = self.cohere_client.embed(
                texts=texts,
                model="embed-english-v3.0",  # Latest model with 1024 dimensions
                input_type="search_document"
            )
            
            return response.embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            raise
    
    def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a query."""
        try:
            response = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",  # Same model as document embeddings
                input_type="search_query"
            )
            
            return response.embeddings[0]
            
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {str(e)}")
            raise
    
    def _create_smart_preview(self, text: str, max_length: int = 300) -> str:
        """Create a smart preview of text that avoids cutting off mid-word/sentence."""
        if len(text) <= max_length:
            return text
        
        # Try to find a good breaking point (sentence ending)
        truncated = text[:max_length]
        
        # Look for sentence endings within a reasonable range
        for ending in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
            last_sentence = truncated.rfind(ending)
            if last_sentence > max_length * 0.7:  # At least 70% of max length
                return text[:last_sentence + 1] + "..."
        
        # Fall back to word boundary
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # At least 80% of max length
            return text[:last_space] + "..."
        
        # Final fallback: hard truncation with ellipsis
        return text[:max_length - 3] + "..."
    
    def _retrieve_documents(self, query: str, n_results: int = None) -> Dict[str, Any]:
        """Retrieve relevant documents for a query."""
        start_time = time.time()
        
        try:
            if n_results is None:
                n_results = int(os.getenv('MAX_RETRIEVAL_DOCS', 5))
            
            # Generate query embedding
            query_embedding = self._generate_query_embedding(query)
            
            # Search vector database
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            retrieval_time = time.time() - start_time
            self.stats['average_retrieval_time'] = (
                (self.stats['average_retrieval_time'] * self.stats['queries_processed'] + retrieval_time) /
                (self.stats['queries_processed'] + 1)
            )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else [],
                'distances': results['distances'][0] if results['distances'] else [],
                'retrieval_time': retrieval_time
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve documents: {str(e)}")
            self.stats['errors'] += 1
            raise
    
    def _generate_response(self, query: str, context_docs: List[str], temperature: Optional[float] = None) -> str:
        """Generate response using Cohere with retrieved context."""
        try:
            # Prepare context from retrieved documents
            context = "\n\n".join(context_docs[:3])  # Use top 3 documents
            effective_temperature = 0.7 if temperature is None else float(temperature)
            
            # Generate response with Cohere Chat API
            response = self.cohere_client.chat(
                model="command-r-08-2024",  # Try a specific version that might still be available
                message=f"""Question: {query}

Context:
{context}

Based on the provided context, please answer the user's question. Use only the information from the context provided. If the context doesn't contain relevant information to answer the question, say so clearly.""",
                max_tokens=300,  # INTENTIONAL ISSUE: Sometimes too short for complete answers
                temperature=effective_temperature,  # Defaults to legacy value unless overridden by API/demo
            )
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            self.stats['errors'] += 1
            raise
    
    def query(self, user_query: str, temperature: Optional[float] = None) -> Dict[str, Any]:
        """Process a user query and return response with metadata."""
        start_time = time.time()
        
        try:
            # Input validation
            if not user_query or not user_query.strip():
                raise ValueError("Empty query provided")
            
            # Retrieve relevant documents
            retrieval_results = self._retrieve_documents(user_query)
            
            # Generate response
            response_text = self._generate_response(
                user_query, 
                retrieval_results['documents'],
                temperature=temperature
            )

            effective_temperature = 0.7 if temperature is None else float(temperature)
            
            # Calculate total response time
            total_time = time.time() - start_time
            
            # Update statistics
            self.stats['queries_processed'] += 1
            self.stats['total_response_time'] += total_time
            
            # Prepare response data
            response_data = {
                'response': response_text,
                'sources': [
                    {
                        'content': self._create_smart_preview(doc),
                        'metadata': meta,
                        'similarity': round(max(0, (1 - dist) * 100), 1)  # Convert cosine distance to similarity percentage
                    }
                    for doc, meta, dist in zip(
                        retrieval_results['documents'][:3],
                        retrieval_results['metadatas'][:3],
                        retrieval_results['distances'][:3]
                    )
                ],
                'retrieval_time': retrieval_results['retrieval_time'],
                'generation_time': total_time - retrieval_results['retrieval_time'],
                'total_time': total_time,
                'temperature': effective_temperature
            }
            
            return response_data
            
        except Exception as e:
            error_time = time.time() - start_time
            self.stats['errors'] += 1
            logger.error(f"Query processing failed: {str(e)}")
            
            return {
                'response': f"I apologize, but I encountered an error processing your query: {str(e)}",
                'sources': [],
                'error': str(e),
                'total_time': error_time
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics for monitoring."""
        avg_response_time = (
            self.stats['total_response_time'] / self.stats['queries_processed']
            if self.stats['queries_processed'] > 0 else 0
        )
        
        return {
            'queries_processed': self.stats['queries_processed'],
            'average_response_time': round(avg_response_time, 3),
            'average_retrieval_time': round(self.stats['average_retrieval_time'], 3),
            'documents_loaded': self.stats['documents_loaded'],
            'error_count': self.stats['errors'],
            'error_rate': (
                self.stats['errors'] / self.stats['queries_processed']
                if self.stats['queries_processed'] > 0 else 0
            )
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of all components."""
        health = {
            'cohere_client': False,
            'vector_db': False,
            'collection': False,
            'documents_loaded': False
        }
        
        try:
            # Test Cohere client
            if self.cohere_client:
                test_response = self.cohere_client.embed(
                    texts=["test"], 
                    model="embed-english-v3.0",  # Same model as main embeddings
                    input_type="search_query"
                )
                health['cohere_client'] = len(test_response.embeddings) > 0
            
            # Test vector database
            if self.vector_db and self.collection:
                health['vector_db'] = True
                health['collection'] = True
                health['documents_loaded'] = self.collection.count() > 0
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
        
        return health