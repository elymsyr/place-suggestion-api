from fastapi import FastAPI
import json, traceback
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter, sleep
import google.generativeai as genai
from KEYS import keys, admin_key, MAPS_API_KEY, GEMINI_API_KEY
from google.ai.generativelanguage_v1beta.types import content
import googlemaps
    
app = FastAPI()

def config_model():
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 1000,
        "response_schema": content.Schema(
            type=content.Type.ARRAY,
            items=content.Schema(
                type=content.Type.OBJECT,
                required=[
                    "place_name",
                    "only_country_name",
                    "only_city_name",
                    "only_district_name",
                    "only_street_name"
                ],
                properties={
                    "place_name": content.Schema(
                        type=content.Type.STRING
                    ),
                    "only_country_name": content.Schema(
                        type=content.Type.STRING
                    ),
                    "only_city_name": content.Schema(
                        type=content.Type.STRING
                    ),
                    "only_district_name": content.Schema(
                        type=content.Type.STRING
                    ),                    
                    "only_street_name": content.Schema(
                        type=content.Type.STRING
                    )
                }
            )
        ),
        "response_mime_type": "application/json",
    }
    return genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=generation_config)

def stream_response(response, start):
    buffer: str = ""
    collecting = False
    for chunk in response:
        # Decode chunk and append it to the buffer
        buffer += chunk if isinstance(chunk, str) else chunk.text
        if not collecting:
            start_index = buffer.find('{')
            if start_index != -1:  # Changed condition to check for a valid start index
                collecting = True
        
        if collecting:
            end_index = buffer.find('}')
            if end_index != -1:  # Changed condition to check for a valid end index
                collecting = False
                start_index = buffer.find('{')
                if start_index != -1:
                    try:
                        response_data = json.loads(buffer[start_index:end_index + 1])
                        buffer = buffer[:start_index] + buffer[end_index + 1:]
                        response_data['timer'] = perf_counter() - start
                        yield response_data
                    except: continue

def scrap(query: str, gemini_api_key: str, max_worker: int, gmaps, location: str = None):
    start = perf_counter()
    genai.configure(api_key=gemini_api_key)
    model = config_model()
    data = {}
    from_api = {}
    with ThreadPoolExecutor(max_workers=int(max_worker)) as executor:
        futures = []
        for chunk in stream_response(model.generate_content(f"{query} (Current location: {location})", stream=True), start=start):
            try:
                places_query = f"{chunk['place_name']}, {chunk['only_street_name']}, {chunk['only_district_name']}, {chunk['only_city_name']}, {chunk['only_country_name']}"
                print(f"Chunk found in {chunk['timer']} s : ", places_query)            
                future = executor.submit(search_google_maps, gmaps, chunk)
                futures.append(future)
            except Exception as e:
                print(e, traceback.format_exc())
        for future in futures:
            json_result, chunk_got = future.result()
            if json_result:
                from_api[f"{chunk_got['place_name']}, {chunk_got['only_street_name']}, {chunk_got['only_district_name']}, {chunk_got['only_city_name']}, {chunk_got['only_country_name']}"] = json_result
    print(f"End : {perf_counter()-start}")
    data['status'] =  1
    data['end_time'] = perf_counter()-start
    data['response'] = from_api
    return data

def search_google_maps(gmaps, chunk):
    try:
        data = gmaps.places(query=f"{chunk['place_name']}", location=f"{chunk['only_district_name']}, {chunk['only_city_name']}, {chunk['only_country_name']}")
        return data, chunk
    except:
        try:
            sleep(0.5)
            data = gmaps.places(query=f"{chunk['place_name']}", location=f"{chunk['only_district_name']}, {chunk['only_city_name']}, {chunk['only_country_name']}")
            return data, chunk
        except:
            try:
                sleep(0.8)
                data = gmaps.places(query=f"{chunk['place_name']}", location=f"{chunk['only_district_name']}, {chunk['only_city_name']}, {chunk['only_country_name']}")            
                return data, chunk
            except:
                return {'status': 'maps api error'}

@app.get("/scrap/")
async def scrape_task(query: str, api_key: str, gemini_api_key: str = None, maps_api_key: str = None, location: str = None, max_worker: int = 6):
    if api_key in keys+[admin_key]:
        if api_key == admin_key:
            if not gemini_api_key: gemini_api_key = GEMINI_API_KEY
            if not maps_api_key: maps_api_key = MAPS_API_KEY
        elif not maps_api_key or not gemini_api_key:
            return{"status": "Authentication error"}
        gmaps = googlemaps.Client(key=maps_api_key)
        return scrap(query=query, gemini_api_key=gemini_api_key, location=location if location else None, max_worker=max_worker, gmaps=gmaps)
    else: return{"status": "Authentication error"}

@app.get("/")
async def read_root():
    return {
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
