import os
import json
import logging
import time
from typing import Dict, Any, List, Optional
from functools import wraps

logger = logging.getLogger(__name__)

def log_execution_time(func):
    """Decorator to log function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {str(e)}")
            raise
    return wrapper

def validate_config():
    """Validate required configuration settings."""
    required_vars = ['COHERE_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    logger.info("Configuration validation passed")

def format_response_metadata(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format response metadata for consistent API responses."""
    return {
        'query_processed_at': time.time(),
        'response_time_ms': round(response_data.get('total_time', 0) * 1000),
        'retrieval_time_ms': round(response_data.get('retrieval_time', 0) * 1000),
        'generation_time_ms': round(response_data.get('generation_time', 0) * 1000),
        'sources_count': len(response_data.get('sources', [])),
        'has_error': 'error' in response_data
    }

def calculate_similarity_score(distance: float) -> float:
    """Convert distance metric to similarity score (0-1)."""
    # Assuming cosine distance, convert to similarity
    return max(0.0, min(1.0, 1.0 - distance))

def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."

def extract_key_phrases(text: str, max_phrases: int = 3) -> List[str]:
    """Extract key phrases from text (simple implementation for demo)."""
    # This is a simplified implementation for demonstration
    # In production, you might use more sophisticated NLP techniques
    sentences = text.split('.')
    phrases = []
    
    for sentence in sentences[:max_phrases]:
        sentence = sentence.strip()
        if len(sentence) > 10:  # Filter out very short sentences
            phrases.append(sentence)
    
    return phrases

def sanitize_query(query: str) -> str:
    """Sanitize user query for safety and processing."""
    # Remove potential harmful characters
    query = query.strip()
    
    # Basic length validation
    if len(query) > 1000:
        query = query[:1000]
        logger.warning("Query truncated due to length limit")
    
    # Remove multiple spaces
    import re
    query = re.sub(r'\s+', ' ', query)
    
    return query

def create_error_response(error_message: str, error_code: str = "PROCESSING_ERROR") -> Dict[str, Any]:
    """Create standardized error response."""
    return {
        'response': f"I apologize, but I encountered an issue: {error_message}",
        'sources': [],
        'error': {
            'message': error_message,
            'code': error_code,
            'timestamp': time.time()
        },
        'metadata': {
            'has_error': True,
            'response_time_ms': 0
        }
    }

def validate_response_quality(response: str, min_length: int = 10) -> Dict[str, Any]:
    """Basic response quality validation."""
    quality_metrics = {
        'length_ok': len(response) >= min_length,
        'has_content': bool(response.strip()),
        'not_error_message': not response.lower().startswith('i apologize'),
        'complete_sentences': response.count('.') > 0 or response.count('!') > 0 or response.count('?') > 0
    }
    
    quality_metrics['overall_quality'] = all([
        quality_metrics['length_ok'],
        quality_metrics['has_content'],
        quality_metrics['complete_sentences']
    ])
    
    return quality_metrics

class ResponseCache:
    """Simple in-memory cache for responses (for demo purposes)."""
    
    def __init__(self, max_size: int = 100, ttl_seconds: int = 300):
        self.cache = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
    
    def get(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached response for query."""
        query_key = self._get_cache_key(query)
        
        if query_key in self.cache:
            cached_item = self.cache[query_key]
            
            # Check if cache entry is still valid
            if time.time() - cached_item['timestamp'] < self.ttl_seconds:
                logger.info(f"Cache hit for query: {query[:50]}...")
                return cached_item['response']
            else:
                # Remove expired entry
                del self.cache[query_key]
        
        return None
    
    def set(self, query: str, response: Dict[str, Any]):
        """Cache response for query."""
        query_key = self._get_cache_key(query)
        
        # Remove oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[query_key] = {
            'response': response,
            'timestamp': time.time()
        }
        
        logger.info(f"Cached response for query: {query[:50]}...")
    
    def _get_cache_key(self, query: str) -> str:
        """Generate cache key from query."""
        import hashlib
        return hashlib.md5(query.lower().encode()).hexdigest()
    
    def clear(self):
        """Clear all cached entries."""
        self.cache.clear()
        logger.info("Response cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'cache_size': len(self.cache),
            'max_size': self.max_size,
            'ttl_seconds': self.ttl_seconds
        }

def setup_logging(level: str = "INFO"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    
    logger.info(f"Logging configured at {level} level")

def load_config_from_file(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.warning(f"Configuration file not found: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
        return {}

def measure_token_usage(text: str) -> int:
    """Estimate token usage for cost tracking (simplified)."""
    # This is a very rough estimation
    # In production, use the actual tokenizer for your model
    return len(text.split()) * 1.3  # Rough approximation

def create_monitoring_metrics() -> Dict[str, Any]:
    """Create basic monitoring metrics structure."""
    return {
        'requests_total': 0,
        'requests_successful': 0,
        'requests_failed': 0,
        'average_response_time': 0.0,
        'total_tokens_used': 0,
        'cache_hit_rate': 0.0,
        'last_error': None,
        'uptime_start': time.time()
    }