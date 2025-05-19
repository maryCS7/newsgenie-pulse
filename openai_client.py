from dotenv import load_dotenv
from openai import OpenAI
import os
import streamlit as st

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(query: str, digest_mode: str, time_of_day: str, tone: str) -> tuple[str, str]:
    print("ask_openai called")
    tone_instructions = {
        "Explain Like I'm Five": "Explain concepts using very simple words and short sentences, as if talking to a 5-year-old child.",
        "Clear & Direct": "Give a concise and straightforward answer, avoiding any fluff or unnecessary details.",
        "Gentle": "Use a kind, friendly, and empathetic tone, with gentle encouragement.",
        "In-Depth / Academic": "Respond with a formal, detailed, and well-structured explanation, including technical terms as needed."
    }.get(tone, "Respond in a natural, neutral tone.")

    system_prompt = (
        f"You are an empathetic AI news assistant helping users stay informed in a personalized, human-friendly way.\n\n"
        f"Respond to the user's query with the following considerations:\n"
        f"- Length/Detail: Based on digest mode: '{digest_mode}'.\n"
        f"- Time of Day: It is currently '{time_of_day}', so match the tone and urgency accordingly.\n"
        f"- Tone Preference: {tone_instructions}\n\n"
        f"Tone examples:\n"
        f"- Explain Like I’m Five: 'Imagine the internet is like a big library...'\n"
        f"- Clear & Direct: 'The main point is...'\n"
        f"- Gentle: 'It's okay to feel overwhelmed, but here is a simple way to think about it...'\n"
        f"- In-Depth / Academic: 'Recent studies in neural networks show that...'\n\n"
        f"Always keep the answer clear, helpful, and aligned with these preferences."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]


    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()

        return answer, system_prompt

    except Exception as e:
        error_msg = f"OpenAI API error: {e}"
        return error_msg, system_prompt
