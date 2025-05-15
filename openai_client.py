from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(query: str, digest_mode: str) -> str:
    messages = [
        {"role": "system", "content": f"Respond in tone and length suitable for mode '{digest_mode}'."},
        {"role": "user", "content": query}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"
