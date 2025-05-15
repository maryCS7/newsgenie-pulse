from router_agent import route_query
import streamlit as st

st.set_page_config(page_title="NewsGenie Pulse", layout="wide")
st.title("🧠 NewsGenie Pulse")

st.sidebar.header("Time of Day")
time_of_day = st.sidebar.radio(
    "What time is it?",
    options=["Morning", "Afternoon", "Evening", "Late Night"],
    help="This helps the assistant adjust tone or energy of responses"
)

st.sidebar.header("Choose Your Mode")
digest_mode = st.sidebar.radio(
    "How are you feeling?",
    options=["I'm Tired", "I've Got 5 Minutes", "Go Deep"],
    help="Select how much news you want and how it's delivered"
)

st.sidebar.header("Tone Preference")
tone = st.sidebar.selectbox(
    "Preferred tone",
    options=["Default", "Casual", "Formal", "Direct", "Simplified"],
    help="How would you like the assistant to speak?"
)

st.sidebar.header("News Preferences")

country = st.sidebar.selectbox(
    "Select a country",
    options={
        "us": "United States",
        "gb": "United Kingdom",
        "ca": "Canada",
        "au": "Australia",
        "in": "India",
        "de": "Germany",
        "fr": "France",
        "jp": "Japan",
        "sg": "Singapore",
        "za": "South Africa"
    }.items(),
    format_func=lambda x: x[1]
)[0] 

category = st.sidebar.selectbox(
    "Select a category",
    options=[
        "technology",
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
    ],
    index=0  # default to 'technology'
)

user_query = st.text_input("Ask a question or request a news topic", "")

if user_query.strip():
    with st.expander("🧠 Agent Response", expanded=True):
        response = route_query(
        user_query,
        digest_mode,
        category=category,
        country=country,
        time_of_day=time_of_day,
        tone=tone
        )
        if response.startswith("OpenAI API error:") or response.startswith("🚨 Failed to fetch news:"):
            st.error(response)
        else:
            st.markdown(response)


