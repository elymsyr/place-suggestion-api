import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


# TODO: Add from https://scrapfly.io/blog/how-to-scrape-google-maps/ in order to search.

def search_google_maps(query, language = 'en'):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)    

    formatted_query = query.replace(' ', '+')
    url = f"https://www.google.com/maps/search/{formatted_query}/?hl={language}"
    print(url)
    # Load the page
    driver.get(url)
    
    try:
        # Example: Wait until an element is present (you can customize this)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'tTVLSc')]"))
        )
        print("Page loaded successfully.")
    except:
        print("Timed out waiting for page to load.")

    # Extract image URL
    prefixes = ("https://lh5.googleusercontent.com/p/", "https://streetviewpixels-pa.googleapis.com")
    image_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tTVLSc')]//img")
    image = [image.get_attribute('src') for image in image_elements if image.get_attribute('src').startswith('test')] if image_elements else None # if image.get_attribute('src').startswith(prefixes)

    # Extract place name
    place_name_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'tTVLSc')]//h1")
    place_name = place_name_elements[0].text if place_name_elements else None

    place_type_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'skqShb')]//button[contains(@class, 'DkEaL')]")
    place_type = place_type_elements[0].text if place_type_elements else None

    if place_type is None or place_type == '':
        place_type_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'skqShb')]")
        place_type = place_type_elements[0].text if place_type_elements else None

    price_elements = driver.find_elements(By.XPATH, "//span[contains(@aria-label, 'Price')]")
    price = price_elements[0].text if price_elements else None

    # Example: Extract some custom data
    data = {
        'image': image,
        'place_name': place_name,
        'place_type': place_type,
        'price': price,
    }

    # Convert the data dictionary to JSON
    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    # Clean up
    # driver.quit()
    # driver.close()
    return json_data

# # Example usage
# query = "Kızılay Meydanı Çankaya Ankara"
# print(search_google_maps(query))

# # Example usage
# query = "St. Antonius Griesbach, Germany"
# print(search_google_maps(query))

# Example usage
query = "La Felicità Paris France"
print(search_google_maps(query))

# Example usage
query = "MAX Premium Burgers Poznań, Poland"
print(search_google_maps(query))

