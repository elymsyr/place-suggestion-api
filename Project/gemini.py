import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

def config_model():
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
    return genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=generation_config)