#!/usr/bin/env python3
"""
Retrieval Strategy Experiments for Students

This experiment demonstrates how different retrieval parameters affect
RAG system performance, including number of documents retrieved,
similarity thresholds, and retrieval strategies.

🎯 Learning Objectives:
- Understand impact of retrieval count on response quality
- Learn about similarity threshold optimization
- Analyze retrieval vs generation trade-offs
- Optimize retrieval strategy for different query types
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag_pipeline import RAGPipeline
import time
import statistics
import chromadb

class RetrievalExperimentPipeline(RAGPipeline):
    """Modified RAG pipeline for retrieval strategy experiments."""
    
    def __init__(self, n_results=5, similarity_threshold=0.0):
        self.experiment_n_results = n_results
        self.experiment_similarity_threshold = similarity_threshold
        # Create unique collection to avoid dimension conflicts
        self.collection_name = f"retrieval_test_{n_results}_{int(similarity_threshold*1000)}"
        super().__init__()
    
    def _initialize_vector_db(self):
        """Initialize ChromaDB with a unique collection for this experiment."""
        try:
            # Create database path for experiment
            db_path = f"./retrieval_experiment_db"
            os.makedirs(db_path, exist_ok=True)
            
            self.vector_db = chromadb.PersistentClient(path=db_path)
            
            # Delete existing collection if it exists
            try:
                self.vector_db.delete_collection(self.collection_name)
            except:
                pass
            
            # Create new collection for this experiment
            self.collection = self.vector_db.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine", "experiment": "retrieval"}
            )
            
            # Load documents
            self._load_documents()
            
            return True
        except Exception as e:
            print(f"Failed to initialize vector database: {str(e)}")
            return False
    
    def _retrieve_documents(self, query, n_results=None):
        """Override to use experimental retrieval parameters."""
        start_time = time.time()
        
        try:
            n_results = self.experiment_n_results
            
            # Generate query embedding
            query_embedding = self._generate_query_embedding(query)
            
            # Search vector database with experimental parameters
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, 20),  # Cap at 20 for performance
                include=["documents", "metadatas", "distances"]
            )
            
            retrieval_time = time.time() - start_time
            
            # Filter by similarity threshold if set
            filtered_docs = []
            filtered_metadata = []
            filtered_distances = []
            
            if results['documents'] and results['distances']:
                for doc, meta, dist in zip(
                    results['documents'][0], 
                    results['metadatas'][0], 
                    results['distances'][0]
                ):
                    # Convert distance to similarity for threshold check
                    similarity = 1 / (1 + (dist / 100))
                    
                    if similarity >= self.experiment_similarity_threshold:
                        filtered_docs.append(doc)
                        filtered_metadata.append(meta)
                        filtered_distances.append(dist)
            
            self.stats['average_retrieval_time'] = (
                (self.stats['average_retrieval_time'] * self.stats['queries_processed'] + retrieval_time) /
                (self.stats['queries_processed'] + 1)
            )
            
            return {
                'documents': filtered_docs,
                'metadatas': filtered_metadata,
                'distances': filtered_distances,
                'retrieval_time': retrieval_time,
                'original_count': len(results['documents'][0]) if results['documents'] else 0,
                'filtered_count': len(filtered_docs)
            }
            
        except Exception as e:
            self.stats['errors'] += 1
            raise

def test_retrieval_strategy(n_results, similarity_threshold, description):
    """Test specific retrieval strategy."""
    print(f"\n{'='*70}")
    print(f"🧪 Testing: {description}")
    print(f"📊 N Results: {n_results}, Similarity Threshold: {similarity_threshold}")
    print(f"{'='*70}")
    
    try:
        pipeline = RetrievalExperimentPipeline(
            n_results=n_results,
            similarity_threshold=similarity_threshold
        )
        
        # Test queries with different retrieval needs
        test_queries = [
            ("Specific", "What is hallucination in GenAI?"),
            ("Broad", "GenAI testing best practices"),
            ("Technical", "RAG evaluation metrics"),
            ("Process", "How to implement continuous testing for AI systems?"),
        ]
        
        results = []
        
        for query_type, query in test_queries:
            print(f"\n📝 {query_type} Query: {query}")
            
            try:
                start_time = time.time()
                result = pipeline.query(query)
                total_time = time.time() - start_time
                
                # Get retrieval info from the last retrieval
                retrieval_info = pipeline._retrieve_documents(query)
                
                similarity_scores = [round(1 / (1 + (d / 100)), 4) for d in retrieval_info['distances']]
                
                result_data = {
                    'query_type': query_type,
                    'query': query,
                    'original_retrieved': retrieval_info['original_count'],
                    'filtered_retrieved': retrieval_info['filtered_count'],
                    'similarity_scores': similarity_scores,
                    'avg_similarity': statistics.mean(similarity_scores) if similarity_scores else 0,
                    'max_similarity': max(similarity_scores) if similarity_scores else 0,
                    'response_length': len(result['response']),
                    'retrieval_time': retrieval_info['retrieval_time'],
                    'total_time': total_time,
                    'sources_used': len(result['sources'])
                }
                
                results.append(result_data)
                
                print(f"   📋 Retrieved: {retrieval_info['original_count']} → {retrieval_info['filtered_count']} (after filtering)")
                print(f"   📊 Similarities: {similarity_scores[:3]}..." if len(similarity_scores) > 3 else f"   📊 Similarities: {similarity_scores}")
                print(f"   🎯 Avg Similarity: {result_data['avg_similarity']:.4f}")
                print(f"   📝 Response Length: {result_data['response_length']} chars")
                print(f"   ⏱️  Times: {retrieval_info['retrieval_time']:.2f}s retrieval, {total_time:.2f}s total")
                
                # Quality indicators
                if retrieval_info['filtered_count'] == 0:
                    print(f"   ⚠️  No documents passed similarity threshold!")
                elif retrieval_info['filtered_count'] < 3:
                    print(f"   📉 Few relevant documents found")
                elif result_data['max_similarity'] < 0.01:
                    print(f"   🎯 Low similarity scores - may need better chunking")
                
                # Add rate limiting delay between queries
                if query_type != "Process":  # Don't wait after the last query
                    print(f"   ⏳ Waiting 5s for rate limiting...")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"   ❌ Query failed: {str(e)}")
                continue
        
        # Calculate overall metrics (only if we have results)
        if not results:
            print(f"\n❌ No successful queries for this retrieval strategy")
            return None
            
        total_retrieved = sum(r['original_retrieved'] for r in results)
        total_filtered = sum(r['filtered_retrieved'] for r in results)
        avg_similarity = statistics.mean([r['avg_similarity'] for r in results if r['avg_similarity'] > 0])
        avg_response_length = statistics.mean([r['response_length'] for r in results])
        avg_retrieval_time = statistics.mean([r['retrieval_time'] for r in results])
        avg_total_time = statistics.mean([r['total_time'] for r in results])
        
        filter_efficiency = (total_filtered / total_retrieved) if total_retrieved > 0 else 0
        
        print(f"\n📊 OVERALL RESULTS:")
        print(f"   📋 Total Documents: {total_retrieved} retrieved → {total_filtered} used")
        print(f"   🎯 Filter Efficiency: {filter_efficiency:.2%}")
        print(f"   📈 Average Similarity: {avg_similarity:.4f}")
        print(f"   📝 Average Response Length: {avg_response_length:.0f} chars")
        print(f"   ⏱️  Average Times: {avg_retrieval_time:.2f}s retrieval, {avg_total_time:.2f}s total")
        
        return {
            'n_results': n_results,
            'similarity_threshold': similarity_threshold,
            'description': description,
            'total_retrieved': total_retrieved,
            'total_filtered': total_filtered,
            'filter_efficiency': filter_efficiency,
            'avg_similarity': avg_similarity,
            'avg_response_length': avg_response_length,
            'avg_retrieval_time': avg_retrieval_time,
            'avg_total_time': avg_total_time,
            'results': results
        }
        
    except Exception as e:
        print(f"❌ Failed to test retrieval strategy: {str(e)}")
        return None

def run_retrieval_experiments():
    """Run retrieval strategy comparison experiments."""
    
    print("🔍 RETRIEVAL STRATEGY EXPERIMENTS")
    print("=" * 80)
    print("Students: Optimize retrieval parameters for better relevance and performance!")
    print("⏰ Note: This experiment includes rate limiting delays (5s between queries)")
    print("   Total experiment time: ~10-15 minutes due to API rate limits")
    print()
    
    # STUDENTS: Different retrieval strategies to test
    retrieval_strategies = [
        # Current default
        (5, 0.0, "Current Strategy (Top 5, No Filtering)"),
        
        # Different retrieval counts
        (3, 0.0, "Strategy 1: Fewer Documents (Top 3)"),
        (7, 0.0, "Strategy 2: More Documents (Top 7)"),
        (10, 0.0, "Strategy 3: Many Documents (Top 10)"),
        (15, 0.0, "Strategy 4: Very Many Documents (Top 15)"),
        
        # With similarity thresholds
        (5, 0.005, "Strategy 5: Quality Filter (Low Threshold)"),
        (5, 0.01, "Strategy 6: Moderate Filter"),
        (5, 0.02, "Strategy 7: High Quality Filter"),
        (10, 0.005, "Strategy 8: More Docs + Quality Filter"),
        
        # Conservative approaches
        (3, 0.01, "Strategy 9: Conservative (Few + High Quality)"),
        (7, 0.005, "Strategy 10: Balanced (Medium + Low Filter)"),
    ]
    
    successful_results = []
    
    for n_results, threshold, description in retrieval_strategies:
        result = test_retrieval_strategy(n_results, threshold, description)
        if result:
            successful_results.append(result)
        
        # Longer pause between strategies to respect rate limits
        print(f"⏳ Waiting 8s before next strategy...")
        time.sleep(8)
    
    if not successful_results:
        print("❌ No retrieval strategies were successful.")
        return
    
    # Compare results
    print(f"\n{'='*120}")
    print("📈 RETRIEVAL STRATEGY COMPARISON RESULTS")
    print(f"{'='*120}")
    
    # Create comprehensive comparison
    print(f"{'Rank':<4} {'Description':<30} {'N':<3} {'Thresh':<7} {'Filter%':<8} {'Avg Sim':<8} {'Resp Len':<8} {'Ret Time':<8} {'Total':<6}")
    print("-" * 120)
    
    # Sort by a composite score (similarity * filter_efficiency - retrieval_time)
    for result in successful_results:
        # Composite score balances quality, efficiency, and speed
        composite_score = (result['avg_similarity'] * 10) + result['filter_efficiency'] - (result['avg_retrieval_time'] / 10)
        result['composite_score'] = composite_score
    
    successful_results.sort(key=lambda x: x['composite_score'], reverse=True)
    
    for i, result in enumerate(successful_results, 1):
        print(f"{i:<4} {result['description'][:29]:<30} {result['n_results']:<3} "
              f"{result['similarity_threshold']:<7} {result['filter_efficiency']:<8.1%} "
              f"{result['avg_similarity']:<8.4f} {result['avg_response_length']:<8.0f} "
              f"{result['avg_retrieval_time']:<8.2f} {result['avg_total_time']:<6.2f}")
    
    if successful_results:
        best_strategy = successful_results[0]
        print(f"\n🏆 BEST RETRIEVAL STRATEGY:")
        print(f"   📊 Configuration: n_results={best_strategy['n_results']}, threshold={best_strategy['similarity_threshold']}")
        print(f"   📝 Description: {best_strategy['description']}")
        print(f"   📋 Documents: {best_strategy['total_retrieved']} retrieved → {best_strategy['total_filtered']} used")
        print(f"   🎯 Filter Efficiency: {best_strategy['filter_efficiency']:.1%}")
        print(f"   📈 Average Similarity: {best_strategy['avg_similarity']:.4f}")
        print(f"   ⏱️  Retrieval Time: {best_strategy['avg_retrieval_time']:.2f}s")
        
        print(f"\n💡 ANALYSIS:")
        if best_strategy['filter_efficiency'] < 0.5:
            print("⚠️  Low filter efficiency - many irrelevant documents retrieved")
        else:
            print("✅ Good filter efficiency - most retrieved documents are relevant")
        
        if best_strategy['avg_similarity'] > 0.01:
            print("✅ Good similarity scores - documents are relevant to queries")
        else:
            print("📈 Low similarity scores - consider improving chunking or embeddings")
        
        if best_strategy['avg_retrieval_time'] > 1.0:
            print("⏱️  Slow retrieval - consider reducing document count")
        else:
            print("✅ Fast retrieval performance")
        
        print(f"\n🔧 TO IMPLEMENT THE BEST STRATEGY:")
        print(f"   1. In app/rag_pipeline.py, find the _retrieve_documents method")
        print(f"   2. Change n_results default from 5 to {best_strategy['n_results']}")
        if best_strategy['similarity_threshold'] > 0:
            print(f"   3. Add similarity filtering with threshold {best_strategy['similarity_threshold']}")
        print(f"   4. Restart the application and test!")

def analyze_query_types():
    """Analyze how different query types perform with various strategies."""
    print(f"\n{'='*80}")
    print("📊 QUERY TYPE ANALYSIS")
    print(f"{'='*80}")
    
    strategies = [
        (3, 0.0, "Conservative: Few docs"),
        (10, 0.0, "Aggressive: Many docs"),
        (5, 0.01, "Filtered: Quality focus"),
    ]
    
    for n_results, threshold, desc in strategies:
        print(f"\n🧪 Testing: {desc}")
        result = test_retrieval_strategy(n_results, threshold, desc)
        
        if result:
            print("\n📊 Per Query Type Performance:")
            for query_result in result['results']:
                print(f"   {query_result['query_type']}: "
                      f"Sim={query_result['avg_similarity']:.4f}, "
                      f"Docs={query_result['filtered_retrieved']}, "
                      f"Time={query_result['total_time']:.2f}s")

if __name__ == "__main__":
    print("Choose experiment type:")
    print("1. Full Retrieval Optimization")
    print("2. Query Type Analysis")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        analyze_query_types()
    else:
        run_retrieval_experiments()