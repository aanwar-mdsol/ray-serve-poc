import httpx
from typing import Optional
from ..shared.models import EmbeddingRequest, EmbeddingResponse
from ..shared.utils import get_logger

logger = get_logger(__name__)


class EmbeddingsClient:
    def __init__(self, embeddings_service_url: str = "http://localhost:8001"):
        """Initialize the embeddings service client."""
        self.base_url = embeddings_service_url
        logger.info(f"Initialized embeddings client with URL: {embeddings_service_url}")
        
        # For Ray deployment, use internal routing
        if embeddings_service_url == "http://localhost:8001":
            import os
            if os.getenv("RAY_SERVE_DEPLOYMENT", "false").lower() == "true":
                self.base_url = "http://localhost:8000/embeddings"
    
    async def get_embeddings(self, text: str, model_name: str = "all-MiniLM-L6-v2") -> Optional[EmbeddingResponse]:
        """Get embeddings from the embeddings service."""
        try:
            request_data = EmbeddingRequest(text=text, model_name=model_name)
            
            async with httpx.AsyncClient() as client:
                logger.info(f"Requesting embeddings for text: {text[:50]}...")
                response = await client.post(
                    f"{self.base_url}/embed",
                    json=request_data.model_dump(),
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                logger.info("Successfully received embeddings from service")
                return EmbeddingResponse(**data)
                
        except httpx.RequestError as e:
            logger.error(f"Network error connecting to embeddings service: {str(e)}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error from embeddings service: {e.response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting embeddings: {str(e)}")
            return None
    
    async def health_check(self) -> bool:
        """Check if the embeddings service is healthy."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health", timeout=5.0)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False
