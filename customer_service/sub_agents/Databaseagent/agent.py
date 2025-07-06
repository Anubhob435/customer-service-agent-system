
"""You are an agent """

from google.adk import Agent
from google.adk.tools import google_search

import logging
from datetime import datetime, timedelta
from google.adk.tools import ToolContext
from pymongo import MongoClient
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def login_enquirey(query: str) -> Dict[str, Any]:
    """
    Function to fetch books from MongoDB database based on query.
    """

    return {}


MODEL = "gemini-2.0-flash"


database_Agent = Agent(
    model=MODEL,
    name="database_agent",
    instruction="You are an agent that can assist withasist with databse operations. ",
    tools=[login_enquirey],
)
