from fastapi import FastAPI, HTTPException
from ..shared.models import UserInputRequest, UserInputResponse
from ..shared.utils import get_logger, create_response
from .client import EmbeddingsClient

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="User Input Service",
    description="Microservice for handling user input and coordinating with embeddings service",
    version="1.0.0"
)

# Initialize embeddings client
embeddings_client = EmbeddingsClient()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    embeddings_healthy = await embeddings_client.health_check()
    return create_response(
        success=True,
        data={
            "user_input_service": "healthy",
            "embeddings_service": "healthy" if embeddings_healthy else "unhealthy"
        },
        message="User input service health check"
    )


@app.post("/process", response_model=UserInputResponse)
async def process_user_input(request: UserInputRequest):
    """Process user input and optionally generate embeddings."""
    try:
        logger.info(f"Processing user input: {request.text[:50]}...")
        
        embeddings_response = None
        
        if request.process_embeddings:
            logger.info("Generating embeddings for user input")
            embeddings_response = await embeddings_client.get_embeddings(request.text)
            
            if embeddings_response is None:
                logger.warning("Failed to get embeddings, continuing without them")
                return UserInputResponse(
                    original_text=request.text,
                    processed=False,
                    embeddings=None,
                    message="Failed to generate embeddings"
                )
        
        response = UserInputResponse(
            original_text=request.text,
            processed=True,
            embeddings=embeddings_response,
            message="Successfully processed user input" + 
                   (" with embeddings" if embeddings_response else " without embeddings")
        )
        
        logger.info("Successfully processed user input")
        return response
        
    except Exception as e:
        logger.error(f"Error processing user input: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint."""
    return create_response(
        success=True,
        data={"service": "user_input"},
        message="User input service is running"
    )
