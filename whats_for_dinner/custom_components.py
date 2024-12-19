from haystack import component
from PIL import Image

import openai
import base64
import io

@component()
class ExtractFoodItemsFromImage:
    """Extracts food ingredients visible in a given image"""

    @component.output_types(answer=str)
    def run(
        self,
        image_path: str,
    ) -> str:
        model = "gpt-4o"

        image_base64 = self.image_to_base64(image_path)

        messages = [
            {
                "role": "user",
                "content": [
                    {
                      "type": "text",
                      "text": "List the visible ingredients as a bullet list."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "high",
                        },
                    }
                ],
            },
        ]

        client = openai

        response = client.chat.completions.create(model=model, messages=messages, stream=False)
        content = response.choices[0].message.content

        return {
            "answer": content,
        }

    def image_to_base64(self, image_path: str) -> str:
        """
        Load an image from the given path and convert it to a base64 string.
        Supports various formats including WEBP, PNG, and JPEG.
        """
        try:
            # Open the image using PIL
            with Image.open(image_path) as img:
                # Convert to RGB if it's not already (e.g., for PNG with transparency)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Create a byte stream
                byte_arr = io.BytesIO()
                # Save as JPEG to the byte stream
                img.save(byte_arr, format='JPEG')
                # Get the byte string
                byte_arr = byte_arr.getvalue()

                # Encode to base64
                return base64.b64encode(byte_arr).decode('utf-8')
        except Exception as e:
            print(f"Error processing image: {e}")
            return None