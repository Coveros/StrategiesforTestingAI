from flask import Flask, render_template, request, jsonify, redirect, url_for, abort
from flask_cors import CORS
import os
import logging
import uuid
from pathlib import Path
from dotenv import load_dotenv
from app.rag_pipeline import RAGPipeline
from app.agentic_testops import TestOpsAgent
import time
import traceback

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
logger = logging.getLogger(__name__)

# Configure Flask with correct template and static directories
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

DOCS_DIR = Path(os.path.dirname(os.path.dirname(__file__))) / 'docs'

EXERCISE_CATALOG = [
    {
        'number': i,
        'student_file': DOCS_DIR / f'Exercise-{i}.md',
        'instructor_file': DOCS_DIR / f'Exercise-{i}-Instructor-Notes.md',
        'student_title': f'Exercise {i}',
        'instructor_title': f'Exercise {i} Instructor Notes',
    }
    for i in range(1, 10)
]

# Initialize RAG pipeline
rag_pipeline = None
agentic_pipeline = TestOpsAgent()


def is_truthy(value) -> bool:
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')

def initialize_rag():
    """Initialize the RAG pipeline with error handling."""
    global rag_pipeline
    try:
        rag_pipeline = RAGPipeline()
        logger.info("RAG pipeline initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
        logger.error(traceback.format_exc())
        return False

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

    role = 'instructor' if instructor_flag else 'student'
    if instructor_flag:
        return redirect(url_for('exercise_view', number=requested_exercise, role=role, instructor='1'))
    return redirect(url_for('exercise_view', number=requested_exercise, role=role))


@app.route('/exercises/<int:number>')
def exercise_view(number: int):
    """Render exercise markdown as a clean in-app page."""
    env_instructor = os.getenv('EXERCISE_HUB_ENABLE_INSTRUCTOR', 'false').strip().lower() == 'true'
    query_instructor = is_truthy(request.args.get('instructor', '0'))
    allow_instructor = env_instructor or query_instructor
    role = str(request.args.get('role', 'student')).strip().lower()
    if role not in ('student', 'instructor'):
        role = 'student'
    if role == 'instructor' and not allow_instructor:
        role = 'student'

    row = next((x for x in EXERCISE_CATALOG if x['number'] == number), None)
    if row is None:
        abort(404)

    target_path = row['student_file'] if role == 'student' else row['instructor_file']
    if not target_path.exists():
        abort(404)

    markdown_content = target_path.read_text(encoding='utf-8')

    prev_num = number - 1 if number > 1 else None
    next_num = number + 1 if number < 9 else None

    return render_template(
        'exercise_hub.html',
        exercise_number=number,
        role=role,
        allow_instructor=allow_instructor,
        instructor_query='1' if query_instructor else None,
        markdown_content=markdown_content,
        exercise_catalog=EXERCISE_CATALOG,
        current_title=row['student_title'] if role == 'student' else row['instructor_title'],
        prev_num=prev_num,
        next_num=next_num,
    )

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests and return responses."""
    start_time = time.time()
    
    try:
        data = request.get_json()
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
                    return jsonify({
                        'error': 'RAG pipeline not available',
                        'status': 'error'
                    }), 500
            
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
        error_msg = f"Error processing query: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        return jsonify({
            'error': error_msg,
            'status': 'error',
            'response_time': round(response_time, 3)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        # Check if RAG pipeline is working
        if rag_pipeline is None:
            if not initialize_rag():
                return jsonify({
                    'status': 'unhealthy',
                    'cohere_client': False,
                    'vector_db': False,
                    'collection': False,
                    'documents_loaded': False,
                    'error': 'Failed to initialize RAG pipeline'
                }), 500
        
        # Get detailed health status from RAG pipeline
        health_status = rag_pipeline.health_check()
        health_status['status'] = 'healthy' if all(health_status.values()) else 'unhealthy'
        
        return jsonify(health_status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'cohere_client': False,
            'vector_db': False,
            'collection': False,
            'documents_loaded': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
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
        return jsonify({'error': str(e)}), 500

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
    
    if not initialize_rag():
        logger.warning("RAG pipeline initialization failed, but starting server anyway")
    
    # Get configuration from environment
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)