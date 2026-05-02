import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import tool
from tavily import TavilyClient
import requests
import schedule
import time
from datetime import datetime

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize clients
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Define tool for Tavily search
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

# Define agents
researcher = Agent(
    role="AI News Researcher",
    goal="Fetch the latest AI news from official AI vendor sources only",
    backstory="You are an expert in gathering factual AI news exclusively from official sources: Google AI, Microsoft Research, OpenAI, Anthropic, Meta AI, Amazon AWS AI, NVIDIA, and other official AI vendor channels. Always cite official sources and avoid third-party or unverified information.",
    model="gpt-4o-mini",
    tools=[search_ai_news]
)

synthesizer = Agent(
    role="News Synthesizer",
    goal="Summarize AI news from official vendor sources into concise, factual reports",
    backstory="You synthesize information accurately from official AI vendor announcements and publications, avoiding hallucinations by sticking strictly to provided facts and citing official sources. Do not invent details or use third-party interpretations.",
    model="gpt-4o-mini"
)

publisher = Agent(
    role="Dev.to Draft Publisher",
    goal="Publish draft posts to dev.to from official AI vendor news summaries only",
    backstory="You prepare and publish draft articles to dev.to sourced exclusively from official AI vendor announcements, ensuring content is clear, accurate, and marked as draft. Only use the publish_devto_draft tool with information from official sources. Do not publish final content immediately.",
    model="gpt-4o-mini",
    tools=[publish_devto_draft]
)

# Define tasks
research_task = Task(
    description="Search for the latest AI news articles from the past 24 hours exclusively from official AI vendor sources: Google AI, Microsoft Research, OpenAI, Anthropic, Meta AI, Amazon AWS AI, NVIDIA, Tesla AI, and other official AI company channels. Focus on official announcements and publications only. Use the search tool to get factual information directly from these vendors. Make sure to include publication dates for each article when available. Provide complete information including titles, dates, summaries, and official source URLs.",
    agent=researcher,
    expected_output="A list of 5-10 recent AI news articles exclusively from official vendor sources with titles, publication dates (when available), summaries, and official URLs. Clearly indicate when dates are not available."
)

synthesize_task = Task(
    description="For each search result returned by the researcher, create an individual concise synthesis. Ensure every synthesis is factual, cites the source, avoids speculation, and is formatted as a standalone summary ready for publication.",
    agent=synthesizer,
    expected_output="A set of individual syntheses, one for each search result, each ready to be published as a dev.to draft."
)

publish_draft_task = Task(
    description="Publish a draft post to dev.to for each synthesized result. For each synthesis, create one draft article with a title, markdown body, tags, sources, and explicit draft status. Return the draft URLs for all created drafts.",
    agent=publisher,
    expected_output="A list of dev.to draft URLs for each published synthesis, or an error message if any publish attempt failed."
)

# Create crew
crew = Crew(
    agents=[researcher, synthesizer, publisher],
    tasks=[research_task, synthesize_task, publish_draft_task]
)

def run_daily_news_agent():
    print("Running daily AI news agent...")
    try:
        result = crew.kickoff()
        result_text = str(result)
        print(result_text)
        
        # Create synthesis directory if it doesn't exist
        synthesis_dir = "synthesis"
        if not os.path.exists(synthesis_dir):
            os.makedirs(synthesis_dir)
        
        # Split result by dev.to URLs to separate syntheses
        draft_urls = [token for token in result_text.split() if token.startswith("https://dev.to/")]
        
        # If there are draft URLs, split the result by them to get individual syntheses
        syntheses = []
        if draft_urls:
            parts = result_text.split("https://dev.to/")
            for i, part in enumerate(parts[1:], 1):  # Skip the first part (before any URL)
                synthesis_with_url = "https://dev.to/" + part
                syntheses.append(synthesis_with_url)
        else:
            # If no URLs found, treat entire result as one synthesis
            syntheses = [result_text]
        
        # Create a file for each synthesis
        date_str = datetime.now().strftime("%Y-%m-%d")
        saved_files = []
        
        for idx, synthesis in enumerate(syntheses, 1):
            filename = os.path.join(synthesis_dir, f"news_synthesis_{date_str}_{idx}.md")
            
            # Remove existing file if it exists to ensure clean recreation
            if os.path.exists(filename):
                os.remove(filename)
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(synthesis)
            
            saved_files.append(filename)
        
        print(f"\n✅ {len(saved_files)} synthesis file(s) saved:")
        for file in saved_files:
            print(f"  - {file}")

        # Print dev.to draft URLs when available
        if draft_urls:
            print("\n✅ Dev.to drafts published at:")
            for url in draft_urls:
                print(f"  - {url}")
    except Exception as e:
        print(f"Error: {e}")

# Schedule to run daily at 8 AM
schedule.every().day.at("08:00").do(run_daily_news_agent)

if __name__ == "__main__":
    # Run once for testing
    run_daily_news_agent()
    # Then schedule
    """ while True:
        schedule.run_pending()
        time.sleep(60) """