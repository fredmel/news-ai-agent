import os
import time
from datetime import datetime
from crewai import Crew

# Import configuration
from .config import SYNTHESIS_DIR

# Import agents
from .agents import researcher, synthesizer, publisher

# Import tasks
from .tasks import research_task, synthesize_task, publish_draft_task

# Create crew
crew = Crew(
    agents=[researcher, synthesizer, publisher],
    tasks=[research_task, synthesize_task, publish_draft_task]
)


def run_daily_news_agent():
    """Execute the daily AI news agent workflow."""
    print("Running daily AI news agent...")
    try:
        result = crew.kickoff()
        result_text = str(result)
        print(result_text)
        
        # Create synthesis directory if it doesn't exist
        if not os.path.exists(SYNTHESIS_DIR):
            os.makedirs(SYNTHESIS_DIR)
        
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
            filename = os.path.join(SYNTHESIS_DIR, f"news_synthesis_{date_str}_{idx}.md")
            
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
