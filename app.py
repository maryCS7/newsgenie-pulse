from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

news_api_key = os.getenv("NEWS_API_KEY")

# title
st.set_page_config(page_title="NewsGenie Pulse", layout="wide")
st.title("🧠 NewsGenie Pulse")

# sidebar: mood/time-based modes
st.sidebar.header("Choose Your Mode")

digest_mode = st.sidebar.radio(
    "How are you feeling?",
    options=["I'm Tired", "I've Got 5 Minutes", "Go Deep"],
    help="Select how much news you want and how it's delivered"
)

# mode customization to-do
st.sidebar.markdown(f"**Selected Mode:** {digest_mode}")

# input
user_query = st.text_input("Ask a question or request a news topic", "")

# trigger response
if st.button("Get Response"):
    if not user_query.strip():
        st.warning("Please enter a question or topic.")
    else:
        with st.spinner("Generating response..."):
            # message adds context for tone/length
            messages = [
                {"role": "system", "content": f"You're an empathetic assistant that tailors responses to the user's selected mode: '{digest_mode}'."},
                {"role": "user", "content": user_query}
            ]

            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.5,
                )
                response_content = response.choices[0].message.content.strip()
                st.success(response_content)

            except Exception as e:
                st.error(f"OpenAI API error: {e}")



