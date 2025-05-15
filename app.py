from openai_client import ask_openai
import streamlit as st



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
            answer = ask_openai(user_query, digest_mode)
            if answer.startswith("OpenAI API error:"):
                st.error(answer)
            else:
                st.success(answer)



