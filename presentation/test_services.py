import asyncio
import httpx


async def test_services():
    """Test both microservices."""
    print("🧪 Testing Ray Embeddings App Services\n")
    
    # Test data
    test_text = "This is a sample text for testing vector embeddings."
    
    try:
        async with httpx.AsyncClient() as client:
            
            # Test User Input Service
            print("Testing User Input Service...")
            user_input_response = await client.post(
                "http://localhost:8000/process",
                json={"text": test_text, "process_embeddings": True},
                timeout=30.0
            )
            
            if user_input_response.status_code == 200:
                data = user_input_response.json()
                print("User Input Service: SUCCESS")
                print(f"   Original text: {data['original_text'][:50]}...")
                print(f"   Processed: {data['processed']}")
                if data['embeddings']:
                    print(f"   Embeddings dimension: {data['embeddings']['dimension']}")
                    print(f"   Model used: {data['embeddings']['model_name']}")
                print()
            else:
                print(f"User Input Service: FAILED (Status: {user_input_response.status_code})")
                print(f"   Error: {user_input_response.text}\n")
            
            # Test Embeddings Service directly
            print("Testing Embeddings Service directly...")
            embeddings_response = await client.post(
                "http://localhost:8001/embed",
                json={"text": test_text},
                timeout=30.0
            )
            
            if embeddings_response.status_code == 200:
                data = embeddings_response.json()
                print("Embeddings Service: SUCCESS")
                print(f"   Text: {data['text'][:50]}...")
                print(f"   Embeddings dimension: {data['dimension']}")
                print(f"   Model used: {data['model_name']}")
                print(f"   First 5 embedding values: {data['embeddings'][:5]}")
                print()
            else:
                print(f"Embeddings Service: FAILED (Status: {embeddings_response.status_code})")
                print(f"   Error: {embeddings_response.text}\n")
            
            # Test health endpoints
            print("Testing Health Endpoints...")

            # User Input Service health
            health_response = await client.get("http://localhost:8000/health")
            if health_response.status_code == 200:
                print("User Input Service Health: OK")
            else:
                print("User Input Service Health: FAILED")

            # Embeddings Service health
            health_response = await client.get("http://localhost:8001/health")
            if health_response.status_code == 200:
                print("Embeddings Service Health: OK")
            else:
                print("Embeddings Service Health: FAILED")

    except httpx.RequestError as e:
        print(f"Network error: {str(e)}")
        print("Make sure the services are running!")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


async def test_ray_services():
    """Test services deployed with Ray Serve."""
    print("Testing Ray Serve Deployed Services\n")
    
    test_text = "Testing Ray Serve deployment with vector embeddings."
    
    try:
        async with httpx.AsyncClient() as client:
            
            # Test User Input Service via Ray
            print("Testing User Input Service via Ray...")
            response = await client.post(
                "http://localhost:8000/api/process",
                json={"text": test_text, "process_embeddings": True},
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("Ray User Input Service: SUCCESS")
                print(f"   Original text: {data['original_text'][:50]}...")
                print(f"   Processed: {data['processed']}")
                if data['embeddings']:
                    print(f"   Embeddings dimension: {data['embeddings']['dimension']}")
                print()
            else:
                print(f"Ray User Input Service: FAILED")
                print(f"   Status: {response.status_code}")
                
            # Test Embeddings Service via Ray
            print("Testing Embeddings Service via Ray...")
            response = await client.post(
                "http://localhost:8000/embeddings/embed",
                json={"text": test_text},
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("Ray Embeddings Service: SUCCESS")
                print(f"   Embeddings dimension: {data['dimension']}")
                print()
            else:
                print(f"Ray Embeddings Service: FAILED")
                print(f"   Status: {response.status_code}")
                
    except Exception as e:
        print(f"Error testing Ray services: {str(e)}")


if __name__ == "__main__":
    print("Choose testing mode:")
    print("1. Test local services (ports 8000, 8001)")
    print("2. Test Ray Serve deployment (port 8000)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(test_services())
    elif choice == "2":
        asyncio.run(test_ray_services())
    else:
        print("Invalid choice. Please run again and select 1 or 2.")
