# Ray Embeddings App

A FastAPI application with vector embeddings generation deployed using Ray Serve. Features two microservices for text processing and embedding generation.

## Architecture

This application consists of two microservices:

1. **Embeddings Service**: Generates vector embeddings from text using sentence-transformers
2. **User Input Service**: Handles user input and coordinates with the embeddings service

## Project Structure

```
ray_basic_app/
├── src/
│   ├── embeddings_service/     # Embeddings microservice
│   │   ├── app.py             # FastAPI app for embeddings
│   │   └── generator.py       # Embedding generation logic
│   ├── user_input_service/     # User input microservice
│   │   ├── app.py             # FastAPI app for user input
│   │   └── client.py          # Client to communicate with embeddings service
│   └── shared/                 # Shared utilities and models
│       ├── models.py          # Pydantic models
│       └── utils.py           # Common utilities
├── deployment/
│   ├── ray_deploy.py              # Ray Serve deployment script
│   └── local_deploy.py            # Local development deployment
├── presentation/
│   ├── demo.py                    # Interactive demo script
│   └── test_services.py           # Service testing script
├── Makefile                   # Development commands
└── docker-compose.yml         # Docker deployment (optional)
```

## Quick Start

### 1. Setup

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install 
    # OR
make dev-setup
```

### 2. Run the Application

**Option A: Local Development (Runs both the Microservices on Separate Ports)**
```bash
make run-local
# or
python local_deploy.py
```
- Embeddings Service: http://localhost:8001
- User Input Service: http://localhost:8000

**Option B: Ray Serve Deployment (Single Port)**
```bash
make run-ray
# or
python ray_deploy.py
```
- All services: http://localhost:8000
- Ray Dashboard: http://localhost:8265

### 3. Test the Services

```bash
# Interactive testing
make test
# or
python test_services.py

# Quick demo
python demo.py
```

## API Endpoints

### Ray Serve Deployment
**User Input Service**
- `GET /api/health` - Health check
- `POST /api/process` - Process user input and generate embeddings

**Embeddings Service**
- `GET /embeddings/health` - Health check
- `POST /embeddings/embed` - Generate embeddings for text

## 💡 Usage Examples

### Basic Text Processing
```bash
curl -X POST http://localhost:8000/process \
  -H 'Content-Type: application/json' \
  -d '{"text": "Hello, world!", "process_embeddings": true}'
```

### Direct Embeddings Generation
```bash
curl -X POST http://localhost:8001/embed \
  -H 'Content-Type: application/json' \
  -d '{"text": "Generate embeddings for this text"}'
```

### Ray Serve Endpoints
```bash
# User input via Ray
curl -X POST http://localhost:8000/api/process \
  -H 'Content-Type: application/json' \
  -d '{"text": "Hello Ray!", "process_embeddings": true}'

# Direct embeddings via Ray
curl -X POST http://localhost:8000/embeddings/embed \
  -H 'Content-Type: application/json' \
  -d '{"text": "Ray embeddings"}'
```

## 🛠️ Development Commands

```bash
make help              # Show all available commands
make install           # Install dependencies
make run-local         # Run services locally
make run-ray           # Deploy with Ray Serve
make test              # Interactive testing
make test-local        # Test local services
make test-ray          # Test Ray deployment
make clean             # Clean up Ray and cache
```

## Configuration

The application uses sensible defaults but can be configured:

- **Embedding Model**: Default is `all-MiniLM-L6-v2` (384 dimensions)
- **Service URLs**: Automatically configured based on deployment mode
- **Logging**: Structured logging with different levels

## Dependencies

Key dependencies:
- **FastAPI**: Web framework for building APIs
- **Ray Serve**: Scalable model serving
- **sentence-transformers**: Pre-trained embedding models
- **httpx**: Async HTTP client for service communication
- **uvicorn**: ASGI server for FastAPI
