import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/"  

def get_news(category=None, query=None, country=None, page_size=5):
    if not NEWS_API_KEY:
        return "🛑 News API key not found."

    if query:
        url = BASE_URL + "everything"
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "pageSize": page_size,
        }
    else:
        url = BASE_URL + "top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "pageSize": page_size,
        }
        if category:
            params["category"] = category
        if country:
            params["country"] = country

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            return f"⚠️ News API error: {data.get('message', 'Unknown error')}"

        articles = data.get("articles", [])
        if not articles:
            return "No news articles found for your query."

        news_summaries = []
        for article in articles:
            title = article.get("title", "No title")
            description = article.get("description", "")
            url = article.get("url", "")
            news_summaries.append(f"**{title}**\n{description}\n[Read more]({url})\n")

        return "\n\n".join(news_summaries)

    except Exception as e:
        return f"🚨 Failed to fetch news: {e}"

