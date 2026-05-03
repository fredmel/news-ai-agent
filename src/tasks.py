"""
Tasks module for AI news agent.
Defines tasks: research, synthesis, and publication.
"""
from crewai import Task
from .agents import researcher, synthesizer, publisher


# Research Task
research_task = Task(
    description="Search for the latest AI news articles from the past 24 hours exclusively from official AI vendor sources: Google AI, Microsoft Research, OpenAI, Anthropic, Meta AI, Amazon AWS AI, NVIDIA, Tesla AI, and other official AI company channels. Focus on official announcements and publications only. Use the search tool to get factual information directly from these vendors. Make sure to include publication dates for each article when available. Provide complete information including titles, dates, summaries, and official source URLs.",
    agent=researcher,
    expected_output="A list of 5-10 recent AI news articles exclusively from official vendor sources with titles, publication dates (when available), summaries, and official URLs. Clearly indicate when dates are not available."
)

# Synthesis Task
synthesize_task = Task(
    description="For each search result returned by the researcher, create an individual concise synthesis. Ensure every synthesis is factual, cites the source, avoids speculation, and is formatted as a standalone summary ready for publication.",
    agent=synthesizer,
    expected_output="A set of individual syntheses, one for each search result, each ready to be published as a dev.to draft."
)

# Publication Task
publish_draft_task = Task(
    description="Publish a draft post to dev.to for each synthesized result. For each synthesis, create one draft article with a title, markdown body, tags, sources, and explicit draft status. Return the draft URLs for all created drafts.",
    agent=publisher,
    expected_output="A list of dev.to draft URLs for each published synthesis, or an error message if any publish attempt failed."
)
