import pytest, sys
from fastapi.testclient import TestClient
sys.path.append('API')
sys.path.append('Test')
sys.path.append('Project')
sys.path.append('API/app')
from main import app # type: ignore
from KEYS import GEMINI_API_KEY, TEST_API_KEY # type: ignore

# Create a TestClient using the FastAPI app
client = TestClient(app)

# Define test data
test_query = "Best places to eat in the world"
test_gemini_api_key = GEMINI_API_KEY
test_api_key = TEST_API_KEY
test_language = "en"
test_max_worker = 2
test_wait_time = 4

# Test the root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Place Suggestion API!",
        "description": "This API provides place suggestions based on user prompts using Gemini AI.",
        "endpoints": {
            "/api/scrape": {
                "method": "GET",
                "description": "Get place suggestions based on a query.",
                "parameters": {
                    "query": "string, required - The search query for place suggestions.",
                    "gemini_api_key": "string, required - Your Gemini API key.",
                    "maps_api_key": "string, optional - Google Maps API key if you want to use Google Maps.",
                    "language": "string, optional - Language code, default is 'en'."
                }
            }
        },
        "author": "@elymsyr",
        "see project": "https://github.com/elymsyr/place-suggestion-api",
        "license": "GNU GENERAL PUBLIC LICENSE"
    }

@pytest.mark.parametrize("query, api_key, gemini_api_key, language, max_worker, wait_time", [
    (test_query, test_api_key, test_gemini_api_key, test_language, test_max_worker, test_wait_time)
])
def test_scrape_task(query, api_key, gemini_api_key, language, max_worker, wait_time):
    url = f"/scrap/?query={query}&api_key={api_key}&gemini_api_key={gemini_api_key}&language={language}&max_worker={max_worker}&wait_time={wait_time}"
    
    response = client.get(url)
    
    index_error = response.text.count('"status": 0')
    index = response.text.count('"status": 1')
    
    print(f"\n{index+index_error} found :\n  Errors : {index_error}\n  Scraped : {index}")
    
    assert index