# GenAI Testing Tutorial - Complete Application

## Overview

This repository is the working codebase and course material for a two-part GenAI testing curriculum.

Part 1 (Exercises 1-4) focuses on RAG testing fundamentals.
Part 2 (Exercises 5-9) focuses on agentic testing for routing, state, reliability, security, and CI gating.

The application is intentionally configured with realistic failure modes so students can practice detection, diagnosis, and mitigation.

## Course Flow

- Student exercises: `docs/Exercise-1.md` to `docs/Exercise-9.md`
- Instructor notes: `docs/Exercise-1-Instructor-Notes.md` to `docs/Exercise-9-Instructor-Notes.md`
- Section transition deck text: `docs/Section-Bridge-RAG-to-Agentic.md`

## Architecture

```
Frontend (HTML/CSS/JS) → Flask Backend → RAG Pipeline → Cohere API
                                    ↓
                               ChromaDB Vector Store
                                    ↑
                            Knowledge Base Documents
```

## Quick Start

### Prerequisites
- Python 3.8+
- Cohere API key (get one at https://cohere.com/)
- 2GB+ RAM for vector database
- Windows PowerShell (for Windows users)

### Installation

1. **Clone and Navigate**
   ```bash
   cd "c:\Users\jpayne\Documents\Training\Notebooks for ML classes\TestingAITutorial"
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv training-env
   training-env\Scripts\activate  # Windows
   # source training-env/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
  copy .env.template .env
   # Edit .env and add your Cohere API key
   ```

   Exercise Hub defaults to Student View only. Set `EXERCISE_HUB_ENABLE_INSTRUCTOR=True` in `.env` only for instructor-led sessions.

   Student agentic access is available via `?agent=1`. Exercise pages automatically pass exercise context back to chat for exercise-aware defaults.

5. **Run Application**
   ```bash
   python run.py
   ```

   If you see `ModuleNotFoundError` (for example `flask_cors`), dependencies were not installed in the interpreter you are using. Re-run:
   ```bash
   python -m pip install -r requirements.txt
   ```

6. **Access Application**
   - Open http://localhost:5000
   - Chat interface should load
   - Try: "What are the key challenges in testing GenAI applications?"
   - Use the bottom **Ask / Agent** toggle in chat to switch modes
   - In Exercise 5-9 flows, Exercise Hub sends `exercise=<n>` so trace/crew defaults can auto-adjust by exercise context

## 🚀 Quick Start (Alternative)

Use the quick launcher:

```bash
python launch.py
```

These provide menu-driven interfaces to:
- Execute regression testing
- Run evaluation framework checks
- Run retrieval tuning support for Exercise 4
- Start the Flask application
- Run Section 7 and 9 automation suites
- Access current exercise documentation

## Project Structure

```
TestingAITutorial/
├── app/
│   ├── __init__.py          # Python package initialization
│   ├── agentic_testops.py   # Agentic backend used in Exercises 5-9
│   ├── main.py              # Flask application and API endpoints
│   ├── rag_pipeline.py      # RAG implementation with Cohere + ChromaDB
│   └── utils.py             # Utility functions and helpers
├── static/
│   ├── css/
│   │   └── style.css        # Professional styling with animations
│   └── js/
│       └── chat.js          # Interactive chat interface logic
├── templates/
│   ├── index.html           # Main chat interface template
│   └── exercise_hub.html    # In-app exercise content renderer
├── data/
│   ├── documents/           # Knowledge base documents (GenAI testing content)
│   │   ├── genai_testing_guide.md
│   │   ├── faq_genai_testing.md
│   │   ├── production_best_practices.md
│   │   └── evaluation_metrics.md
│   └── chroma_db/          # Vector database storage (auto-created)
├── tests/
│   └── evaluation_framework.py      # Advanced evaluation tools
├── experiments/             # Exercise support experiments
│   ├── __init__.py          # Package initialization
│   ├── retrieval_experiments.py    # Document retrieval optimization
├── regression_testing/      # Regression testing framework for Exercise 3
│   ├── __init__.py         # Package initialization
│   ├── regression_testing.py       # Core framework
│   └── config.json         # Configurable thresholds and settings
├── docs/                   # Course materials and instructor notes
│   ├── Exercise-1.md ... Exercise-9.md
│   ├── Exercise-1-Instructor-Notes.md ... Exercise-9-Instructor-Notes.md
│   ├── Section-Bridge-RAG-to-Agentic.md
├── section7_nfr_quickrun.py # Exercise 7 automation artifact generator
├── section9_agentic_test_suite.py # Exercise 9 CI-style artifact generator
├── temperature_demo.py      # Exercise 1 temperature variability demo
├── requirements.txt         # Python dependencies
├── .env.template           # Environment variable template  
├── run.py                  # Application entry point
├── launch.py               # Interactive launcher menu
└── README.md               # This file (main project overview)
```

## Features

### 🤖 **RAG Chatbot**
- **Cohere Integration**: Uses Cohere's embeddings and Command model
- **ChromaDB Vector Store**: Local, persistent document storage
- **Custom Python RAG Pipeline**: Purpose-built for classroom testing exercises
- **Source Attribution**: Shows retrieved documents and similarity scores
- **Real-time Performance Metrics**: Response times and statistics

### 🎨 **Professional Frontend**
- **Modern UI**: Clean, responsive design with animations
- **Real-time Chat**: WebSocket-like experience with fetch API
- **Message History**: Persistent chat sessions
- **Loading States**: Typing indicators and progress feedback
- **Statistics Dashboard**: System health and performance metrics
- **Mobile Responsive**: Works on all device sizes

### 🧪 **Comprehensive Testing Suite**
- **Exercise 3 evaluation framework**: `tests/evaluation_framework.py`
- **Exercise 3 regression framework**: `regression_testing/regression_testing.py`
- **Exercise 4 tuning support**: `experiments/retrieval_experiments.py`
- **Exercise 7 automation artifacts**: `section7_nfr_quickrun.py`
- **Exercise 9 CI-style gate artifacts**: `section9_agentic_test_suite.py`

### 📚 **Rich Knowledge Base**
- **GenAI Testing Guide**: Comprehensive testing strategies
- **FAQ**: Common questions about GenAI testing
- **Best Practices**: Production deployment guidelines
- **Evaluation Metrics**: Detailed metric explanations
- **Real-world Examples**: Practical testing scenarios

## Course Quick Reference

### Exercise Progression
- Exercises 1-4: RAG testing (goldens, evaluation, diagnostics)
- Section bridge: `docs/Section-Bridge-RAG-to-Agentic.md`
- Exercises 5-9: Agentic testing (routing, trajectories, NFR, red teaming, CI gating)

### Core Scripts
- App: `python run.py`
- Launcher: `python launch.py`
- Section 7 quick-run: `python section7_nfr_quickrun.py`
- Section 9 CI suite: `python section9_agentic_test_suite.py`

### Essential Endpoints
- `GET /` chat UI
- `POST /api/chat` message processing
- `GET /api/health` service health

### Environment Setup
- Copy `.env.template` to `.env`
- Set `COHERE_API_KEY` in `.env`

## Usage Examples

### Basic Chat Testing
```bash
curl -X POST http://localhost:5000/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is hallucination in GenAI?"}'
```

### Running Exercise 3 Frameworks
```bash
# Run evaluation framework
python tests/evaluation_framework.py

# Run regression testing framework
python -m regression_testing.regression_testing
```

### Running Exercise 4 Retrieval Tuning Support
```bash
python experiments/retrieval_experiments.py
```

### Running Exercise 7 and 9 Automation
```bash
python section7_nfr_quickrun.py
python section9_agentic_test_suite.py
```

### Quality Assessment
```python
from tests.evaluation_framework import EvaluationFramework
from app.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
evaluator = EvaluationFramework(pipeline)

# Run comprehensive evaluation
results = evaluator.evaluate_response_quality([
    {"query": "What is GenAI testing?", "expected_topics": ["testing", "genai"]}
])

print(f"Average Quality Score: {results['average_quality_score']}")
```

### Regression Testing Integration
```python
from regression_testing.regression_testing import RegressionTestFramework

# Create framework
framework = RegressionTestFramework()

# Run tests programmatically
results = framework.run_regression_tests(save_results=True)

# Check quality gate
gate_passed = (
    results['summary']['pass_rate'] >= 0.8 and 
    results['summary']['critical_failures'] == 0
)

print(f"Quality Gate: {'PASSED' if gate_passed else 'FAILED'}")
```

## Learning Paths

### 🎓 **Beginner Track**
1. Complete student labs in order: Exercise 1 -> 4 (RAG section)
2. Deliver the section bridge before starting Exercise 5
3. Complete Exercise 5 -> 9 (agentic section)
4. Use Section 7 and 9 automation scripts for standardized evidence

### 🔬 **Intermediate Track**  
1. Map each exercise deliverable to one reusable rubric/checklist
2. Add 2-3 custom prompts per exercise to extend coverage
3. Compare baseline and post-change behavior using quick-run artifacts
4. Create a release recommendation from Exercise 9 evidence

### 🚀 **Advanced Track**
1. Extend `section7_nfr_quickrun.py` with additional NFR scenarios
2. Extend `section9_agentic_test_suite.py` with new showstopper gates
3. Integrate suite outputs into CI (artifact upload + gate decision)
4. Add production monitoring and drift checks aligned to Exercise 9

## Troubleshooting

### Common Setup Issues

**"ModuleNotFoundError: No module named 'app' or 'regression_testing'"**
- Ensure commands are run from repository root
- Use the launcher (`python launch.py`) or run `python -m regression_testing.regression_testing`

**"KeyError: 'failed_tests' or 'avg_response_length'"**
- These issues have been FIXED in the test framework
- Test data now includes all required keys for proper execution

**"Import cohere could not be resolved"**
- Ensure virtual environment is activated: `training-env\Scripts\activate`
- Run `pip install -r requirements.txt`
- Use `python launch.py` to run exercise workflows consistently

**"sentence-transformers not available"**
- This package is optional but recommended for semantic similarity scoring in Exercise 3
- Install with `pip install sentence-transformers` (or `pip install -r requirements.txt`)
- If unavailable, the regression framework still runs with reduced semantic checks

**"COHERE_API_KEY not found"**
- Copy `.env.template` to `.env`
- Add your Cohere API key to the `.env` file

**"ChromaDB initialization failed"**
- Ensure you have write permissions in the project directory
- Delete `data/chroma_db/` folder and restart if corrupted

**"Flask app won't start"**
- Check that port 5000 is available
- Set `FLASK_PORT=5001` in `.env` to use a different port

### Performance Issues

**Slow first response**
- First query initializes the vector database (expected delay)
- Subsequent queries should be faster

**High memory usage**
- ChromaDB loads embeddings into memory
- Reduce document collection size if needed

### Quality Issues

**Poor response quality**
- This may be intentional! Part of the learning exercise
- Check if you're discovering the planted issues correctly

**Off-topic responses**
- Test the system's domain boundaries
- Document cases where it should vs. shouldn't know answers

## Educational Value

This application provides hands-on experience with:

### 🎯 **Core Concepts**
- **Non-deterministic Testing**: Dealing with probabilistic outputs
- **Quality vs. Performance Trade-offs**: Balancing response quality and speed
- **Evaluation Metrics**: Understanding different ways to measure success
- **Production Readiness**: What it takes to deploy GenAI systems

### 🛡️ **Safety and Robustness**
- **Hallucination Detection**: Identifying when AI generates false information
- **Bias Testing**: Checking for unfair or inappropriate responses  
- **Edge Case Handling**: System behavior with unusual inputs
- **Adversarial Robustness**: Resistance to malicious inputs

### 📈 **Performance Engineering**
- **Latency Optimization**: Making responses faster
- **Scalability Testing**: Handling multiple concurrent users
- **Resource Management**: Efficient use of CPU, memory, and API calls
- **Monitoring and Alerting**: Detecting issues in production

### 🔍 **Quality Assurance**
- **Multi-dimensional Evaluation**: Beyond simple accuracy metrics
- **Consistency Testing**: Ensuring reliable behavior
- **Regression Detection**: Catching quality degradation
- **User Experience Focus**: Testing from the user's perspective

## Contributing

This is an educational project. If you find additional issues or have suggestions for improvements:

1. Document your findings clearly
2. Propose educational value of the change
3. Consider impact on learning objectives
4. Share with the instructor or class

## License

This project is created for educational purposes. Use freely for learning and teaching GenAI testing concepts.

---

**Happy Testing!** 🧪🤖

Remember: The goal isn't just to build GenAI applications, but to build ones that are reliable, safe, and provide genuine value to users. Testing is how we ensure that promise is kept.