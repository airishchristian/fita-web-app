import base64
import json
from anthropic import Anthropic
import config
from dotenv import load_dotenv
import os
load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def identify_food(image):
    # Encode image to base64
    image_bytes = image.read()
    image_data = base64.b64encode(image_bytes).decode("utf-8")

    # Get the image media type
    media_type = image.type

    # Send to Claude Vision
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": """Identify this food and estimate its macros.
                        Respond ONLY in JSON format like this, no extra text:
                        {
                            "food_name": "name of the food",
                            "calories": 000,
                            "protein": 00,
                            "carbs": 00,
                            "fat": 00
                        }"""
                    }
                ]
            }
        ]
    )

    # Parse the response
    result = response.content[0].text
    clean = result.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)