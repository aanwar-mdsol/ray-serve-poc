import ray
from ray import serve
import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.embeddings_service.app import app as embeddings_app
from src.user_input_service.app import app as user_input_app


@serve.deployment(
    name="embeddings-service",
    num_replicas=1,
    ray_actor_options={"num_cpus": 1, "num_gpus": 0}
)
@serve.ingress(embeddings_app)
class EmbeddingsService:
    pass


@serve.deployment(
    name="user-input-service", 
    num_replicas=1,
    ray_actor_options={"num_cpus": 1, "num_gpus": 0}
)
@serve.ingress(user_input_app)
class UserInputService:
    pass


async def deploy_services():
    """Deploy both microservices using Ray Serve."""
    print("Starting Ray Serve deployment...")
    
    # Set environment variable for Ray deployment
    os.environ["RAY_SERVE_DEPLOYMENT"] = "true"
    
    # Initialize Ray
    if not ray.is_initialized():
        ray.init()
    
    # Deploy the embeddings service
    print("Deploying embeddings service...")
    embeddings_handle = serve.run(
        EmbeddingsService.bind(),
        name="embeddings-service",
        route_prefix="/embeddings"
    )
    
    # Deploy the user input service  
    print("Deploying user input service...")
    user_input_handle = serve.run(
        UserInputService.bind(),
        name="user-input-service", 
        route_prefix="/api"
    )

    print("Both services deployed successfully!")
    print("Service endpoints:")
    print("   • Embeddings Service: http://localhost:8000/embeddings")
    print("   • User Input Service: http://localhost:8000/api")
    print("   • Ray Dashboard: http://localhost:8265")
    
    return embeddings_handle, user_input_handle


if __name__ == "__main__":
    try:
        # Run the deployment
        handles = asyncio.run(deploy_services())

        print("\nServices are now running!")
        print("Try these endpoints:")
        print("   curl -X POST http://localhost:8000/api/process -H 'Content-Type: application/json' -d '{\"text\": \"Hello world!\"}'")
        print("   curl -X POST http://localhost:8000/embeddings/embed -H 'Content-Type: application/json' -d '{\"text\": \"Hello world!\"}'")
        print("\nPress Ctrl+C to stop the services")

        # Keep the script running
        try:
            while True:
                asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down services...")
            serve.shutdown()
            ray.shutdown()
            print("Services stopped successfully!")

    except Exception as e:
        print(f"Error during deployment: {str(e)}")
        if ray.is_initialized():
            ray.shutdown()
        sys.exit(1)
