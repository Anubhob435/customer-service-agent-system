
"""websearch_agent for finding anything on the web using Google Search."""

from google.adk import Agent
from google.adk.tools import google_search



MODEL = "gemini-2.5-flash"


academic_websearch_agent = Agent(
    model=MODEL,
    name="websearch_agent",
    instruction="You are a web search agent that can find information on the web using Google Search. You can answer questions, find articles, and retrieve information from the internet.",
    tools=[google_search],
)
