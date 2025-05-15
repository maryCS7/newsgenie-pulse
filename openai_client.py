from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(query: str, digest_mode: str, time_of_day: str = None, tone: str = None) -> str:
    system_prompt = f"Respond in tone and length suitable for mode '{digest_mode}'."
    if tone and tone != "Default":
        system_prompt += f" Use a {tone.lower()} tone."
    if time_of_day:
        system_prompt += f" It's currently {time_of_day.lower()} — adjust the tone or energy accordingly."

    messages = [
    {"role": "system", "content": system_prompt},
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
