from flask import Flask, render_template, request, jsonify, redirect, url_for, abort, send_file
from flask_cors import CORS
import os
import logging
import uuid
import hmac
from pathlib import Path
from dotenv import load_dotenv
from app.rag_pipeline import RAGPipeline
from app.agentic_testops import TestOpsAgent
import time
import traceback
from collections import defaultdict, deque
from functools import wraps

# Load environment variables from project root for consistent behavior
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

# Configure logging
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)

# Configure Flask with correct template and static directories
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

try:
    _max_request_bytes = int(os.getenv('MAX_REQUEST_BYTES', '65536'))
except ValueError:
    _max_request_bytes = 65536
app.config['MAX_CONTENT_LENGTH'] = min(max(_max_request_bytes, 1024), 1048576)

try:
    CHAT_MAX_CHARS = int(os.getenv('CHAT_MAX_CHARS', '2000'))
except ValueError:
    CHAT_MAX_CHARS = 2000

# Restrict cross-origin API access to configured trusted origins.
_cors_origins_raw = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000')
_cors_origins = [origin.strip() for origin in _cors_origins_raw.split(',') if origin.strip()]
CORS(app, resources={r"/api/*": {"origins": _cors_origins}})

DOCS_DIR = Path(os.path.dirname(os.path.dirname(__file__))) / 'docs'
EXERCISE_DOCS_DIR = DOCS_DIR / 'exercises'
TRACE_SAMPLES_DIR = Path(os.path.dirname(os.path.dirname(__file__))) / 'artifacts' / 'trace_samples'

EXERCISE_CATALOG = [
    {
        'number': i,
        'student_file': EXERCISE_DOCS_DIR / f'Exercise-{i}.md',
        'instructor_file': EXERCISE_DOCS_DIR / f'Exercise-{i}-Instructor-Notes.md',
        'student_title': f'Exercise {i}',
        'instructor_title': f'Exercise {i} Instructor Notes',
    }
    for i in range(1, 10)
]

# Initialize RAG pipeline
rag_pipeline = None
agentic_pipeline = TestOpsAgent()
_rate_limit_buckets = defaultdict(deque)
_last_rag_init_error = None


def is_truthy(value) -> bool:
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')


def should_expose_diagnostics() -> bool:
    return is_truthy(os.getenv('EXPOSE_DIAGNOSTIC_DETAILS', 'false'))


def _client_ip() -> str:
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def rate_limit(scope: str, max_requests: int, window_seconds: int):
    """Simple in-memory per-IP limiter for exposed endpoints."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = f"{scope}:{_client_ip()}"
            bucket = _rate_limit_buckets[key]

            while bucket and now - bucket[0] > window_seconds:
                bucket.popleft()

            if len(bucket) >= max_requests:
                retry_after = max(1, int(window_seconds - (now - bucket[0])))
                return jsonify({
                    'error': 'Rate limit exceeded. Please retry later.',
                    'status': 'error',
                    'retry_after_seconds': retry_after,
                }), 429

            bucket.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def _extract_admin_token() -> str:
    auth_header = request.headers.get('Authorization', '').strip()
    if auth_header.lower().startswith('bearer '):
        return auth_header[7:].strip()
    return request.headers.get('X-Admin-Token', '').strip()


def require_admin_token():
    configured_token = os.getenv('APP_ADMIN_TOKEN', '').strip()
    require_token = is_truthy(os.getenv('RESET_REQUIRE_ADMIN_TOKEN', 'true'))

    if not configured_token:
        if require_token:
            logger.warning('APP_ADMIN_TOKEN is not configured; denying sensitive reset action')
            return False, (jsonify({
                'error': 'Sensitive action not configured',
                'status': 'error',
            }), 503)

        logger.warning('APP_ADMIN_TOKEN is not configured; allowing reset because RESET_REQUIRE_ADMIN_TOKEN is false')
        return True, None

    presented_token = _extract_admin_token()
    if not presented_token or not hmac.compare_digest(presented_token, configured_token):
        return False, (jsonify({
            'error': 'Unauthorized',
            'status': 'error',
        }), 401)

    return True, None

def initialize_rag():
    """Initialize the RAG pipeline with error handling."""
    global rag_pipeline, _last_rag_init_error
    try:
        rag_pipeline = RAGPipeline()
        _last_rag_init_error = None
        logger.info("RAG pipeline initialized successfully")
        return True
    except Exception as e:
        _last_rag_init_error = str(e)
        logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
        logger.error(traceback.format_exc())
        return False


@app.after_request
def add_security_headers(response):
    response.headers.setdefault('X-Content-Type-Options', 'nosniff')
    response.headers.setdefault('X-Frame-Options', 'DENY')
    response.headers.setdefault('Referrer-Policy', 'no-referrer')
    if request.path.startswith('/api/'):
        response.headers.setdefault('Cache-Control', 'no-store')
    return response

@app.route('/')
def index():
    """Serve the main chat interface."""
    instructor_mode = is_truthy(request.args.get('instructor', '0'))

    return render_template(
        'index.html',
        instructor_mode=instructor_mode,
    )


@app.route('/exercises')
def exercises_home():
    """Redirect to first exercise in student view."""
    instructor_flag = is_truthy(request.args.get('instructor', '0'))
    try:
        requested_exercise = int(request.args.get('exercise', 1))
    except (TypeError, ValueError):
        requested_exercise = 1

    if requested_exercise < 1 or requested_exercise > 9:
        requested_exercise = 1

    role = 'student'
    if instructor_flag:
        return redirect(url_for('exercise_view', number=requested_exercise, role=role, instructor='1'))
    return redirect(url_for('exercise_view', number=requested_exercise, role=role))


@app.route('/exercises/<int:number>')
def exercise_view(number: int):
    """Render exercise markdown as a clean in-app page."""
    env_instructor = os.getenv('EXERCISE_HUB_ENABLE_INSTRUCTOR', 'false').strip().lower() == 'true'
    query_instructor = is_truthy(request.args.get('instructor', '0'))
    instructor_mode = env_instructor or query_instructor
    role = 'student'

    row = next((x for x in EXERCISE_CATALOG if x['number'] == number), None)
    if row is None:
        abort(404)

    target_path = row['student_file']
    if not target_path.exists():
        abort(404)

    markdown_content = target_path.read_text(encoding='utf-8')

    prev_num = number - 1 if number > 1 else None
    next_num = number + 1 if number < 9 else None

    return render_template(
        'exercise_hub.html',
        exercise_number=number,
        role=role,
        allow_instructor=False,
        instructor_mode=instructor_mode,
        instructor_query='1' if query_instructor else None,
        markdown_content=markdown_content,
        exercise_catalog=EXERCISE_CATALOG,
        current_title=row['student_title'],
        prev_num=prev_num,
        next_num=next_num,
    )

@app.route('/api/chat', methods=['POST'])
@rate_limit('chat', max_requests=30, window_seconds=60)
def chat():
    """Handle chat requests and return responses."""
    start_time = time.time()
    
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'status': 'error'
            }), 415

        data = request.get_json(silent=True)
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided',
                'status': 'error'
            }), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'error': 'Empty message provided',
                'status': 'error'
            }), 400

        if len(user_message) > CHAT_MAX_CHARS:
            return jsonify({
                'error': f'Message exceeds limit of {CHAT_MAX_CHARS} characters',
                'status': 'error'
            }), 400

        mode = str(data.get('mode', 'rag')).strip().lower()
        if mode not in ('rag', 'agentic'):
            return jsonify({
                'error': "Invalid mode. Use 'rag' or 'agentic'",
                'status': 'error'
            }), 400

        session_id = str(data.get('session_id') or uuid.uuid4())
        include_trace = bool(data.get('include_trace', False))
        crew_mode = bool(data.get('crew_mode', False))

        requested_temperature = None
        if 'temperature' in data and data['temperature'] is not None:
            try:
                requested_temperature = float(data['temperature'])
            except (TypeError, ValueError):
                return jsonify({
                    'error': 'Invalid temperature value. Must be a number between 0.0 and 1.0',
                    'status': 'error'
                }), 400

            if requested_temperature < 0.0 or requested_temperature > 1.0:
                return jsonify({
                    'error': 'Temperature out of range. Use a value between 0.0 and 1.0',
                    'status': 'error'
                }), 400
        
        if mode == 'agentic':
            # Process with the test-ops agentic loop
            response_data = agentic_pipeline.process(
                user_message,
                session_id=session_id,
                include_trace=include_trace,
                crew_mode=crew_mode
            )
        else:
            # Check if RAG pipeline is initialized
            if rag_pipeline is None:
                if not initialize_rag():
                    error_payload = {
                        'error': 'RAG pipeline not available',
                        'next_step': 'Verify Ollama is running, model is pulled, and restart the app',
                        'status': 'error'
                    }
                    if should_expose_diagnostics() and _last_rag_init_error:
                        error_payload['details'] = _last_rag_init_error
                    return jsonify(error_payload), 500
            
            # Get response from RAG pipeline
            response_data = rag_pipeline.query(user_message, temperature=requested_temperature)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Add metadata to response
        response_data['response_time'] = round(response_time, 3)
        response_data['status'] = 'success'
        response_data['mode'] = mode
        response_data['session_id'] = session_id
        
        logger.info(f"Query processed successfully in {response_time:.3f}s")
        return jsonify(response_data)
        
    except Exception as e:
        response_time = time.time() - start_time
        error_ref = uuid.uuid4().hex[:8]
        logger.error(f"Error processing query [{error_ref}]: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'error': f'Request processing failed (ref: {error_ref})',
            'status': 'error',
            'response_time': round(response_time, 3)
        }), 500

@app.route('/api/health', methods=['GET'])
@rate_limit('health', max_requests=60, window_seconds=60)
def health_check():
    """Health check endpoint."""
    try:
        # Check if RAG pipeline is working
        if rag_pipeline is None:
            if not initialize_rag():
                error_payload = {
                    'status': 'unhealthy',
                    'provider_client': False,
                    'vector_db': False,
                    'collection': False,
                    'documents_loaded': False,
                    'error': 'Failed to initialize RAG pipeline',
                }
                if should_expose_diagnostics() and _last_rag_init_error:
                    error_payload['details'] = _last_rag_init_error
                return jsonify(error_payload), 500
        
        # Get detailed health status from RAG pipeline
        health_status = rag_pipeline.health_check()
        # Connection status should represent core service connectivity, not content readiness.
        core_connected = (
            bool(health_status.get('provider_client'))
            and bool(health_status.get('vector_db'))
            and bool(health_status.get('collection'))
        )

        health_status['status'] = 'healthy' if core_connected else 'unhealthy'
        health_status['core_connected'] = core_connected
        health_status['warnings'] = []

        if core_connected and not bool(health_status.get('documents_loaded')):
            health_status['warnings'].append('Knowledge base is empty; retrieval quality may be reduced.')
        
        return jsonify(health_status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'unhealthy',
            'provider_client': False,
            'vector_db': False,
            'collection': False,
            'documents_loaded': False,
            'error': 'Health check failed'
        }), 500

@app.route('/api/stats', methods=['GET'])
@rate_limit('stats', max_requests=30, window_seconds=60)
def get_stats():
    """Get pipeline statistics for testing purposes."""
    try:
        rag_stats = {}
        if rag_pipeline is not None:
            rag_stats = rag_pipeline.get_stats()

        agentic_stats = agentic_pipeline.get_stats()

        return jsonify({
            'rag': rag_stats,
            'agentic': agentic_stats,
            # Preserve legacy top-level keys for existing UI compatibility
            'queries_processed': rag_stats.get('queries_processed', 0),
            'average_response_time': rag_stats.get('average_response_time', 0),
            'documents_loaded': rag_stats.get('documents_loaded', 0),
            'error_rate': rag_stats.get('error_rate', 0),
        })
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'Failed to retrieve stats'}), 500


@app.route('/trace-demo', methods=['GET'])
def trace_demo():
    """Serve the most recent trace visualization HTML artifact."""
    try:
        if not TRACE_SAMPLES_DIR.exists():
            return jsonify({
                'status': 'error',
                'error': 'Trace samples directory not found',
                'next_step': 'Run: python trace_visualization_demo.py'
            }), 404

        html_files = sorted(
            TRACE_SAMPLES_DIR.glob('trace_visualization_*.html'),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        if not html_files:
            return jsonify({
                'status': 'error',
                'error': 'No trace visualization report found',
                'next_step': 'Run: python trace_visualization_demo.py'
            }), 404

        response = send_file(html_files[0], mimetype='text/html')
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        logger.error(f"Error loading trace demo: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'error': 'Failed to load trace demo report'
        }), 500


@app.route('/api/reset', methods=['POST'])
@rate_limit('reset', max_requests=5, window_seconds=60)
def reset_state():
    """Reset session or full agentic in-memory state for deterministic reruns."""
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'status': 'error'
            }), 415

        authorized, denial_response = require_admin_token()
        if not authorized:
            return denial_response

        data = request.get_json(silent=True) or {}
        scope = str(data.get('scope', 'session')).strip().lower()
        reset_breaker = bool(data.get('reset_circuit_breaker', True))

        if scope not in ('session', 'all'):
            return jsonify({
                'error': "Invalid scope. Use 'session' or 'all'",
                'status': 'error'
            }), 400

        if scope == 'session':
            session_id = str(data.get('session_id', '')).strip()
            if not session_id:
                return jsonify({
                    'error': "session_id is required when scope='session'",
                    'status': 'error'
                }), 400
            result = agentic_pipeline.reset_session_state(session_id, reset_circuit_breaker=reset_breaker)
        else:
            result = agentic_pipeline.reset_all_state(reset_circuit_breaker=reset_breaker)

        return jsonify({
            'status': 'success',
            'result': result,
        })
    except Exception as e:
        logger.error(f"Error resetting state: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Failed to reset state',
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize RAG pipeline on startup
    logger.info("Starting GenAI Testing Tutorial Application...")
    logger.info(
        "Runtime diagnostics: python=%s env_file=%s exists=%s",
        os.sys.executable,
        PROJECT_ROOT / '.env',
        (PROJECT_ROOT / '.env').exists(),
    )
    
    if not initialize_rag():
        logger.warning("RAG pipeline initialization failed, but starting server anyway")
    
    # Get configuration from environment
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)