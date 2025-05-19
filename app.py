import streamlit as st
from router_agent import route_query

st.set_page_config(page_title="NewsGenie Pulse", layout="wide")
st.title("🧠 NewsGenie Pulse")

with st.sidebar:
    with st.expander("Time & Mood Settings", expanded=True):
        time_of_day = st.radio(
            "What time is it?",
            options=["Morning", "Afternoon", "Evening", "Late Night"],
            help="This helps the assistant adjust tone or energy of responses"
        )

        digest_mode = st.radio(
            "How are you feeling?",
            options=["I'm Tired", "I've Got 5 Minutes", "Go Deep"],
            help="Select how much news you want and how it's delivered"
        )

        tone = st.selectbox(
            "Preferred tone",
            options=["Gentle", "Clear & Direct", "Explain Like I'm Five", "In-Depth / Academic"],
            help="How would you like the assistant to speak?"
        )
    st.markdown("---")

    with st.expander("News Preferences", expanded=True):
        country = st.selectbox(
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

        category = st.selectbox(
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
            index=0
        )

user_query = st.text_input("Ask a question or request a news topic", "")

if user_query.strip():
    with st.expander("🧠 Personalized Summary", expanded=True):
        result = route_query(
            user_query,
            digest_mode,
            category=category,
            country=country,
            time_of_day=time_of_day,
            tone=tone
        )
        print("Result from route_query:", result)

        summary, articles, system_prompt = result

        print("System prompt sent to OpenAI:")
        print(system_prompt)

        st.markdown(summary)


    if articles:
        with st.expander("📰 View Source Articles"):
            for a in articles:
                st.markdown(f"**[{a['title']}]({a['url']})**\n\n{a['description']}")

