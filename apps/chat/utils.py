import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_chatgpt_response(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer",
                "content": "You are a helpful assistant for a team of marketing people. They work for AdSphere, a marketing company that specializes in marketing campaigns for small to mid business. They can do ads on social media, billboards, radio, and similar. You need to act as a marketing guru.",
            },
            {
                "role": "user",
                "content": f"{message}",
            },
        ],
        max_tokens=1000,
    )
    return response.choices[0].message.content


def generate_image(description):
    response = client.images.generate(prompt=description, n=1, size="512x512")
    return response.data[0].url
