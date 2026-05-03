"""
Tools module for AI news agent.
Defines Tavily search and Dev.to publishing tools.
"""
import requests
from crewai.tools import tool
from .config import tavily_client, DEVTO_API_KEY


@tool
def search_ai_news(query: str) -> str:
    """Search for AI news using Tavily."""
    response = tavily_client.search(query=query, search_depth="advanced")
    results = response.get("results", [])
    news_list = []
    for result in results[:10]:  # Limit to 10 results
        title = result.get('title', 'No title')
        content = result.get('content', 'No content')
        url = result.get('url', 'No URL')
        
        # Try multiple date fields that might be available
        published_date = (result.get('published_date') or 
                         result.get('date') or 
                         result.get('pub_date') or 
                         'Date not available')
        
        # Format date if available
        if published_date != 'Date not available':
            try:
                # Try to parse and format the date
                from datetime import datetime
                # Handle different date formats
                if isinstance(published_date, str):
                    # If it's already a readable date string, keep it
                    if len(published_date) > 10:  # Likely includes time
                        published_date = published_date[:10]  # Keep only date part
            except:
                pass  # Keep original date if parsing fails
        
        news_list.append(f"Title: {title}\nDate: {published_date}\nSummary: {content}\nURL: {url}\n")
    return "\n".join(news_list)


@tool
def publish_devto_draft(headline: str, body_markdown: str, tags: list[str] | None = None) -> str:
    """Publish a draft article to dev.to using the DEVTO_API_KEY."""
    if not DEVTO_API_KEY:
        return "Error: DEVTO_API_KEY is not set."

    payload = {
        "article": {
            "title": headline,
            "body_markdown": body_markdown,
            "published": False,
            "tags": tags or ["ai", "news"],
        }
    }
    headers = {
        "Content-Type": "application/json",
        "api-key": DEVTO_API_KEY,
    }
    response = requests.post("https://dev.to/api/articles", json=payload, headers=headers)
    if response.status_code not in (200, 201):
        return f"Error publishing draft: {response.status_code} {response.text}"
    data = response.json()
    return data.get("url", "Draft created, URL unavailable")
