from openai_client import ask_openai
from news_api import get_news

# def route_query(user_query, mode, category=None, country=None, time_of_day=None, tone=None):
#     """
#     Agentic router: decide API call based on query and mode.
#     """
#     query_lower = user_query.lower()

#     news_keywords = ["news", "headlines", "latest", "update", "happening"]
#     wants_news = any(kw in query_lower for kw in news_keywords) or category or country

#     if wants_news and mode != "Go Deep":
#         # news API call except Go Deep mode
#         return get_news(query=user_query, category=category, country=country, page_size=5)

#     if mode == "Go Deep":
#         # RAG here
#         # For now, fallback to GPT but add a prefix to clarify
#         prompt = f"(Deep mode enabled) {user_query}"
#         return ask_openai(prompt, mode)

#     # default: simple GPT call
#     return ask_openai(user_query, mode, time_of_day, tone)

def route_query(user_query, mode, category=None, country=None, time_of_day=None, tone=None):
    """
    Agentic router: decide API call based on query and mode.
    Always returns: (summary, articles, system_prompt, metadata)
    """
    query_lower = user_query.lower()

    news_keywords = ["news", "headlines", "latest", "update", "happening"]
    wants_news = any(kw in query_lower for kw in news_keywords) or category or country

    if wants_news and mode != "Go Deep":
        # Call get_news which returns (articles, system_prompt, metadata)
        articles, system_prompt, metadata = get_news(query=user_query, category=category, country=country, page_size=5)
        
        # Generate empathetic AI summary based on articles
        summary = ask_openai(user_query, mode, time_of_day, tone, articles)

        return summary, articles, system_prompt, metadata

    if mode == "Go Deep":
        # RAG here or fallback to GPT with prompt
        prompt = f"(Deep mode enabled) {user_query}"
        summary = ask_openai(user_query, mode, time_of_day, tone)
        return summary, [], prompt, {}

    # default GPT call
    summary = ask_openai(user_query, mode, time_of_day, tone)
    print("SUMMARY RETURNED IN route_query:", summary)
    print("TONE", tone)
    print("MODE", mode)
    return summary, [], "Standard prompt", {}

