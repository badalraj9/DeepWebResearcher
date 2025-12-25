import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def test_openrouter():
    """Test OpenRouter integration"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please add your OpenRouter API key to the .env file")
        return False
    
    try:
        # Test OpenRouter connection
        print(f"Testing with key: {api_key[:5]}...{api_key[-5:]}")
        llm = ChatOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            model="xiaomi/mimo-v2-flash:free",  # User specified model
            temperature=0.1,
            max_tokens=1000
        )
        
        # Simple test message
        print("Sending request...")
        response = llm.invoke("Hello! Please respond with 'OpenRouter is working correctly' if you can see this message.")
        
        print("✅ OpenRouter integration test successful!")
        print(f"Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_openrouter()
