url = 'http://3.64.193.28:80/'
query = 'Find me top 3 restaunts in New York'

import requests
from KEYS import GEMINI_API_KEY

response = requests.get(url=url) # params={'query':query, 'gemini_api_key':GEMINI_API_KEY}

print(response)