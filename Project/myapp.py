import json, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import traceback
from KEYS import *
from gemini import chat_session, model
from fastapi import FastAPI
from io import StringIO
from fastapi.responses import StreamingResponse

app = FastAPI()

def extract_coordinates(text):
    # Regular expression patterns for both formats
    pattern_1 = r'!3d([-+]?\d*\.\d+)!4d([-+]?\d*\.\d+)!'  # Pattern for '!3d<lat>!4d<lon>!'
    pattern_2 = r'@([-+]?\d*\.\d+),([-+]?\d*\.\d+),'       # Pattern for '@<lat>,<lon>,'
    
    # Check the text against both patterns
    match_1 = re.search(pattern_1, text)
    match_2 = re.search(pattern_2, text)
    
    if match_1:
        # Extract coordinates from the first pattern
        latitude, longitude = match_1.groups()
    elif match_2:
        # Extract coordinates from the second pattern
        latitude, longitude = match_2.groups()
    else:
        # Return None if no coordinates found
        return None

    return float(latitude), float(longitude)

def fetch_place_data(query, language):
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/?hl=en"
    json_result = search_google_maps(url=url)
    if json_result:
        json_result['coordinate'] = extract_coordinates(json_result['url'])
    return query, json_result

def stream_response(response):
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
                        yield response_data
                    except: continue

def scrape(query, language='en'):
    result = {}
    
    # Use ThreadPoolExecutor for parallel fetching
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        
        # Consume the stream response as it arrives
        for chunk in stream_response(model.generate_content(f"{query} ({language=})", stream=True)):
                # Process the chunk (convert it to JSON)
            try:
                # Extract the places query from the chunk
                places_query = f"{chunk['place_name']}, {chunk['street']}, {chunk['city']}, {chunk['country']}"

                future = executor.submit(fetch_place_data, places_query, language)
                futures.append(future)

            except Exception as e:
                print(e, traceback.format_exc())

        # Collect results from futures as they complete
        for future in futures:
            query, json_result = future.result()
            if json_result:
                yield f"{json_result['place_name']}: {json.dumps(json_result)}\n"

def search_google_maps(url):
    start = perf_counter()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data = {}
    try:
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'tTVLSc')]")))
        WebDriverWait(driver, 30).until(lambda driver: driver.current_url.startswith('https://www.google.com/maps/place'))
        data['url'] = driver.current_url
        print("Page loaded successfully.")
    except:
        print("Timed out waiting for page to load.")
        return None

    # Extract place name
    place_name_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tTVLSc')]//h1")
    place_name = place_name_elements[0].text if place_name_elements else None
    
    prefixes = ("https://lh5.googleusercontent.com/p/", "https://streetviewpixels-pa.googleapis.com")
    image_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tTVLSc')]//img")
    image = [image.get_attribute('src') for image in image_elements if image.get_attribute('src').startswith(prefixes)] if image_elements else None # if image.get_attribute('src').startswith(prefixes)

    place_type_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'skqShb')]//button[contains(@class, 'DkEaL')]")
    place_type = place_type_elements[0].text if place_type_elements else None

    if place_type is None or place_type == '':
        place_type_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'skqShb')]")
        place_type = place_type_elements[0].text if place_type_elements else None

    price_elements = driver.find_elements(By.XPATH, "//span[contains(@aria-label, 'Price')]")
    price = price_elements[0].text if price_elements else None


    data['place_name'] = place_name
    data['place_type'] = place_type
    data['image'] = image
    data['price'] = price
    print("Page parsed and scraped ", perf_counter() - start)
    return data

@app.get("/scrap/")
async def scrape_task(query: str, language: str = 'en'):
    return StreamingResponse(scrape(query, language), media_type="text/event-stream")
