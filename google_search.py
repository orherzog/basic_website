import os
import requests

def google_search(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,  # Search query
        "key": api_key,  # Your API key
        "cx": cse_id,  # Your Custom Search Engine ID
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json()
        return results.get("items", [])
    else:
        print(f"Error: {response.status_code}")
        return []

# Get the API key and CSE ID from environment variables
api_key = os.getenv("GOOGLE_API_KEY")  # Fetch API key from environment variable
cse_id = os.getenv("GOOGLE_CSE_ID")  # Fetch CSE ID from environment variable

query = "abc"

results = google_search(query, api_key, cse_id)

if results:
    for index, result in enumerate(results):
        print(f"{index+1}. Title: {result['title']}")
        print(f"   Link: {result['link']}")
else:
    print("No results found.")