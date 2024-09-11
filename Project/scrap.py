from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Path to your web driver executable
webdriver_path = 'path/to/chromedriver'

# Initialize the web driver
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service)

try:
    # Open the initial URL
    initial_url = 'https://www.google.com/maps/search/Stone+Bridge,+Adana,+Turkey/?hl=en'
    driver.get(initial_url)

    # Wait for the URL to change (adjust the condition as needed)
    WebDriverWait(driver, 30).until(lambda driver: driver.current_url != initial_url)

    # Print the final URL
    final_url = driver.current_url
    print(f"Final URL: {final_url}")

finally:
    # Close the browser
    driver.quit()
