from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from ..shared.utils import get_logger

logger = get_logger(__name__)


class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding generator with a pre-trained model."""
        self.model_name = model_name
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info(f"Model {model_name} loaded successfully")
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        try:
            logger.info(f"Generating embeddings for text: {text[:50]}...")
            embeddings = self.model.encode([text])
            return embeddings[0].tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_dimension(self) -> int:
        """Get the dimension of the embeddings."""
        return self.model.get_sentence_embedding_dimension()
