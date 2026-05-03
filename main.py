"""
Main entry point for the AI News Agent.
Imports and runs the agent from the src module.
"""
import schedule
import time

from src.main import run_daily_news_agent
from src.config import SCHEDULE_TIME

# Schedule to run daily at configured time
schedule.every().day.at(SCHEDULE_TIME).do(run_daily_news_agent)

if __name__ == "__main__":
    # Run once for testing
    run_daily_news_agent()
    # Then schedule
    """ while True:
        schedule.run_pending()
        time.sleep(60) """