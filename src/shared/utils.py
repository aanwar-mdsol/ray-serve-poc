import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(name)


def create_response(success: bool, data: Any = None, message: str = "") -> Dict[str, Any]:
    """Create a standardized API response."""
    return {
        "success": success,
        "data": data,
        "message": message
    }
