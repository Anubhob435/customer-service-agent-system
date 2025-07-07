
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
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['customer_service']
        collection = db['users']
        
        # Search for username in the database
        user = collection.find_one({"username": query})
        
        if user:
            logger.info(f"User found: {query}")
            return {
                "status": "success",
                "message": f"Username '{query}' found in database",
                "user_exists": True,
                "username": user.get("username")
            }
        else:
            logger.info(f"User not found: {query}")
            return {
                "status": "not_found",
                "message": f"Username '{query}' not found in database",
                "user_exists": False
            }
            
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return {
            "status": "error",
            "message": f"Database error: {str(e)}",
            "user_exists": False
        }
    finally:
        if 'client' in locals():
            client.close()



MODEL = "gemini-2.0-flash"


database_Agent = Agent(
    model=MODEL,
    name="database_agent",
    instruction="You are an agent that can assist withasist with databse operations. ",
    tools=[login_enquirey],
)
