from fastapi import FastAPI, HTTPException
from ..shared.models import EmbeddingRequest, EmbeddingResponse
from ..shared.utils import get_logger, create_response
from .generator import EmbeddingGenerator

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Embeddings Service",
    description="Microservice for generating vector embeddings",
    version="1.0.0"
)

# Initialize embedding generator
embedding_generator = EmbeddingGenerator()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return create_response(
        success=True,
        message="Embeddings service is healthy"
    )


@app.post("/embed", response_model=EmbeddingResponse)
async def generate_embeddings(request: EmbeddingRequest):
    """Generate embeddings for the provided text."""
    try:
        logger.info(f"Received embedding request for text: {request.text[:50]}...")
        
        # Generate embeddings
        embeddings = embedding_generator.generate_embeddings(request.text)
        dimension = embedding_generator.get_dimension()
        
        response = EmbeddingResponse(
            text=request.text,
            embeddings=embeddings,
            model_name=request.model_name,
            dimension=dimension
        )
        
        logger.info(f"Successfully generated embeddings with dimension: {dimension}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing embedding request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint."""
    return create_response(
        success=True,
        data={"service": "embeddings"},
        message="Embeddings service is running"
    )
