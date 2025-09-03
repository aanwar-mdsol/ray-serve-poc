#!/usr/bin/env python3
"""
Quick demo script to test the Ray Embeddings App
"""
import asyncio
import httpx
import json


async def demo_local_services():
    """Demo the local services (ports 8000 and 8001)"""
    print("🎯 Demo: Local Services")
    print("=" * 50)
    
    test_texts = [
        "Machine learning is transforming industries",
        "Ray makes distributed computing easier",
        "FastAPI provides fast web APIs"
    ]
    
    async with httpx.AsyncClient() as client:
        for i, text in enumerate(test_texts, 1):
            print(f"\n{i}. Testing: '{text}'")
            
            try:
                # Test user input service
                response = await client.post(
                    "http://localhost:8000/process",
                    json={"text": text, "process_embeddings": True},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Processed successfully")
                    if data.get('embeddings'):
                        dim = data['embeddings']['dimension']
                        print(f"   📊 Generated {dim}-dimensional embeddings")
                        print(f"   🔢 Sample values: {data['embeddings']['embeddings'][:3]}")
                    else:
                        print(f"   ⚠️  No embeddings: {data.get('message', 'Unknown')}")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    
            except httpx.RequestError as e:
                print(f"   ❌ Connection error: {e}")
                print("   💡 Make sure to run: python local_deploy.py")


async def demo_ray_services():
    """Demo the Ray Serve deployment"""
    print("\n🎯 Demo: Ray Serve Deployment")
    print("=" * 50)
    
    test_text = "Ray Serve makes deploying ML models simple"
    
    async with httpx.AsyncClient() as client:
        try:
            # Test via Ray Serve
            response = await client.post(
                "http://localhost:8000/api/process",
                json={"text": test_text, "process_embeddings": True},
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Ray deployment working!")
                print(f"📝 Text: {data['original_text']}")
                if data.get('embeddings'):
                    print(f"📊 Embeddings dimension: {data['embeddings']['dimension']}")
                    print(f"🧠 Model: {data['embeddings']['model_name']}")
                else:
                    print(f"⚠️  {data.get('message', 'No embeddings generated')}")
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except httpx.RequestError as e:
            print(f"❌ Connection error: {e}")
            print("💡 Make sure to run: python ray_deploy.py")


def print_usage():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("🚀 Ray Embeddings App - Quick Start")
    print("=" * 60)
    print("\n📋 Available commands:")
    print("   make run-local    # Run services locally (ports 8000, 8001)")
    print("   make run-ray      # Deploy with Ray Serve (port 8000)")
    print("   make test         # Interactive testing")
    print("   python demo.py    # This demo script")
    
    print("\n🔧 Manual commands:")
    print("   python local_deploy.py     # Local deployment")
    print("   python ray_deploy.py       # Ray deployment")
    print("   python test_services.py    # Interactive tests")
    
    print("\n📚 Endpoints:")
    print("   Local Mode:")
    print("     • User Input:  http://localhost:8000/process")
    print("     • Embeddings:  http://localhost:8001/embed")
    print("   Ray Mode:")
    print("     • User Input:  http://localhost:8000/api/process")
    print("     • Embeddings:  http://localhost:8000/embeddings/embed")


async def main():
    """Main demo function"""
    print("🎮 Ray Embeddings App Demo")
    print("Choose demo mode:")
    print("1. Local services (separate ports)")
    print("2. Ray Serve deployment")
    print("3. Show usage info")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            await demo_local_services()
        elif choice == "2":
            await demo_ray_services()
        elif choice == "3":
            print_usage()
        else:
            print("Invalid choice")
            print_usage()
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
