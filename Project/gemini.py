import os, json
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import KEYS

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
    "response_schema": content.Schema(
        type=content.Type.ARRAY,
        items=content.Schema(
            type=content.Type.OBJECT,
            required=[
                "place_name",
                "country",
                "city",
                "street"
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
                "street": content.Schema(
                    type=content.Type.STRING
                )
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

# while True:
#     input_text = input('input:  ')
    
#     response = chat_session.send_message(input_text)

#     data = json.loads(response.text)
#     print(type(data))

#     print(json.dumps(data, indent=4))