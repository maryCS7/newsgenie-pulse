import streamlit as st
import json
import ast
from router_agent import route_query

def parse_article(article):
    """Converts article to dict if it's a JSON or Python string."""
    if isinstance(article, dict):
        return article
    if isinstance(article, str):
        try:
            return json.loads(article)
        except json.JSONDecodeError:
            try:
                return ast.literal_eval(article)
            except Exception:
                return None
    return None

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

        print("🔍 RAW RESULT:", result)
        print("TYPE OF RESULT:", type(result))
        print("LENGTH OF RESULT:", len(result))

        if not isinstance(result, (list, tuple)) or len(result) != 4:
            st.error(f"❌ route_query() returned unexpected format: {result}")
            st.stop()

        summary, articles, system_prompt, metadata = result
        print("SUMMARY RETURNED in APP:", summary)
        print("SUMMARY TYPE", type(summary))
        if isinstance(summary, tuple):
            summary = summary[0]
        
        st.markdown(summary.replace('\\n', '\n').strip())

    if articles:
        with st.expander("📰 View Source Articles"):
            for i, raw_article in enumerate(articles):
                article = parse_article(raw_article)
                if isinstance(article, dict) and all(k in article for k in ("title", "url", "description")):
                    st.markdown(f"**[{article['title']}]({article['url']})**\n\n{article['description']}")
                else:
                    st.warning(f"⚠️ Skipping malformed article at index {i}")
                    st.code(raw_article)
    else:
        st.info("No articles available.")




