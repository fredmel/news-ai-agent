"""
Configuration module for loading environment variables and initializing clients.
"""
import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# Configuration constants
SYNTHESIS_DIR = "synthesis"
SCHEDULE_TIME = "08:00"
