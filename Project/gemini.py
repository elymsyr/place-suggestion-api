import os, json
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import KEYS

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type=content.Type.ARRAY,
        items=content.Schema(
            type=content.Type.OBJECT,
            required=[
                "place_name",
                "country",
                "city",
                "coordinates_N",
                "coordinates_E"
            ],
            properties={
                "place_name": content.Schema(
                    type=content.Type.STRING
                ),
                "country": content.Schema(
                    type=content.Type.STRING
                ),
                "city": content.Schema(
                    type=content.Type.STRING
                ),
                "coordinates_N": content.Schema(
                    type=content.Type.NUMBER,
                    format="float"
                ),
                "coordinates_E": content.Schema(
                    type=content.Type.NUMBER,
                    format="float"
                ),
            }
        )
    ),
    "response_mime_type": "application/json",
}



model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat()

while True:
    input_text = input('input:  ')
    
    response = chat_session.send_message(input_text)

    data = json.loads(response.text)

    print(json.dumps(data, indent=4))