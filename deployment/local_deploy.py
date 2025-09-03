import uvicorn
import multiprocessing
import sys
import os
import time

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def run_embeddings_service():
    """Run the embeddings service on port 8001."""
    uvicorn.run(
        "src.embeddings_service.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )


def run_user_input_service():
    """Run the user input service on port 8000."""
    # Wait a bit for embeddings service to start
    time.sleep(3)
    uvicorn.run(
        "src.user_input_service.app:app", 
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    print("Starting FastAPI services locally...")
    print("Embeddings Service will run on: http://localhost:8001")
    print("User Input Service will run on: http://localhost:8000")
    
    try:
        # Start both services as separate processes
        embeddings_process = multiprocessing.Process(target=run_embeddings_service)
        user_input_process = multiprocessing.Process(target=run_user_input_service)
        
        embeddings_process.start()
        user_input_process.start()
        
        print("Both services started successfully!")
        print("\nTry these endpoints:")
        print("   curl -X POST http://localhost:8000/process -H 'Content-Type: application/json' -d '{\"text\": \"Hello world!\"}'")
        print("   curl -X POST http://localhost:8001/embed -H 'Content-Type: application/json' -d '{\"text\": \"Hello world!\"}'")
        print("\nPress Ctrl+C to stop the services")

        # Wait for both processes
        embeddings_process.join()
        user_input_process.join()
        
    except KeyboardInterrupt:
        print("\nShutting down services...")
        embeddings_process.terminate()
        user_input_process.terminate()
        embeddings_process.join()
        user_input_process.join()
        print("Services stopped successfully!")
    except Exception as e:
        print(f"Error starting services: {str(e)}")
        sys.exit(1)
