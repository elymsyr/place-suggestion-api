import json, re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import googlemaps
from time import perf_counter
from KEYS import *
from gemini import chat_session

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

def scrap(query, language = 'en'):
    start = perf_counter()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)  
    print("Driver set ", perf_counter()-start) ; start = perf_counter()
    
    result: dict = {}
    response = chat_session.send_message(f"{query}   ({language=})")
    response_data: list  = json.loads(response.text)
    places_query: dict = {data['place_name']: f"{data['place_name']}, {data['city']}, {data['country']}" for data in response_data}
    print(places_query)
    print("Gemini response ", perf_counter()-start) ; start = perf_counter()
    
    for name, query in places_query.items():
        url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/?hl=en"
        json_result = search_google_maps(url=url, driver=driver, language=language, place_name_control=name)
        if json_result:
            json_result['coordinate'] = extract_coordinates(json_result['url'])
            result[query] = json_result

    print("Dictionary set ", perf_counter()-start)
    
    return result

def search_google_maps(url, driver, place_name_control, language):
    driver.get(url)
    data = {}
    try:
        # Example: Wait until an element is present (you can customize this)
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
    
    if place_name: print(place_name_control.strip().lower(), place_name.strip().lower())
    # if place_name is None or (not place_name_control.strip().lower() in place_name.strip().lower()): # or place_name.strip().lower() in 'results'
    #     return None

    # Extract image URL
    prefixes = ("https://lh5.googleusercontent.com/p/", "https://streetviewpixels-pa.googleapis.com")
    image_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tTVLSc')]//img")
    image = [image.get_attribute('src') for image in image_elements if image.get_attribute('src').startswith('test')] if image_elements else None # if image.get_attribute('src').startswith(prefixes)

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

    # Convert the data dictionary to JSON
    # json_data = json.dumps(data, indent=4, ensure_ascii=False)
    return data

# # Example usage
# query = "Kızılay Meydanı Çankaya Ankara"
# print(search_google_maps(query))

# # Example usage
# query = "St. Antonius Griesbach, Germany"
# print(search_google_maps(query))

# # Example usage
# query = "La Felicità Paris France"
# print(search_google_maps(query))

# # Example usage
# query = "MAX Premium Burger Poznań, Poland"
# print(search_google_maps(query))

data = scrap('Best places to see in Çukurova, Adana')
print(json.dumps(data, indent=4, ensure_ascii=False))