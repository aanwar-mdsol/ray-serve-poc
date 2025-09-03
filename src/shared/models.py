from pydantic import BaseModel
from typing import List, Optional


class EmbeddingRequest(BaseModel):
    text: str
    model_name: Optional[str] = "all-MiniLM-L6-v2"


class EmbeddingResponse(BaseModel):
    text: str
    embeddings: List[float]
    model_name: str
    dimension: int


class UserInputRequest(BaseModel):
    text: str
    process_embeddings: bool = True


class UserInputResponse(BaseModel):
    original_text: str
    processed: bool
    embeddings: Optional[EmbeddingResponse] = None
    message: str
