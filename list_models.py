
import os
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("API Key not found")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    print("Listing models...")
    # List models method might vary slightly in v1beta/v1
    # Try the client method directly if possible, or standard way
    # The client object structure depends on library version. 
    # Let's try standard client.models.list()
    
    # We need to see what methods are available on client
    # But usually it's client.models.list()
    
    # The new google-genai library (v0.x) uses specific methods.
    # checking documentation or guessing based on error message 'Call ListModels'.
    
    # Let's try to list models using iterate
    for m in client.models.list():
        print(f"Model: {m.name}")
        if 'generateContent' in m.supported_generation_methods:
             print(f"  - Supports generateContent")

except Exception as e:
    print(f"Error: {e}")
