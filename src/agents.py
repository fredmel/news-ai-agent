"""
Agents module for AI news agent.
Defines AI agents: researcher, synthesizer, and publisher.
"""
from crewai import Agent
from .tools import search_ai_news, publish_devto_draft


# AI News Researcher Agent
researcher = Agent(
    role="AI News Researcher",
    goal="Fetch the latest AI news from official AI vendor sources only",
    backstory="You are an expert in gathering factual AI news exclusively from official sources: Google AI, Microsoft Research, OpenAI, Anthropic, Meta AI, Amazon AWS AI, NVIDIA, and other official AI vendor channels. Always cite official sources and avoid third-party or unverified information.",
    model="gpt-4o-mini",
    tools=[search_ai_news]
)

# News Synthesizer Agent
synthesizer = Agent(
    role="News Synthesizer",
    goal="Summarize AI news from official vendor sources into concise, factual reports",
    backstory="You synthesize information accurately from official AI vendor announcements and publications, avoiding hallucinations by sticking strictly to provided facts and citing official sources. Do not invent details or use third-party interpretations.",
    model="gpt-4o-mini"
)

# Dev.to Publisher Agent
publisher = Agent(
    role="Dev.to Draft Publisher",
    goal="Publish draft posts to dev.to from official AI vendor news summaries only",
    backstory="You prepare and publish draft articles to dev.to sourced exclusively from official AI vendor announcements, ensuring content is clear, accurate, and marked as draft. Only use the publish_devto_draft tool with information from official sources. Do not publish final content immediately.",
    model="gpt-4o-mini",
    tools=[publish_devto_draft]
)
