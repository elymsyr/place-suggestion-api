url = 'http://0.0.0.0:80/scrap'
query = 'Find me top 3 restaunts in New York'

import requests
from KEYS import GEMINI_API_KEY

response = requests.get(url=url, params={'query':query, 'gemini_api_key':GEMINI_API_KEY})
