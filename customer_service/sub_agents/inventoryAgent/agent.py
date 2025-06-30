
"""You are an agent that can assist with checking and updating inventory of books in a library. 
You can also assist with checking the availability of books, updating the inventory, 
and providing information about books in the library."""

from google.adk import Agent
from google.adk.tools import google_search

import logging
from datetime import datetime, timedelta
from google.adk.tools import ToolContext
from pymongo import MongoClient
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def inventory_operations(query: str) -> Dict[str, Any]:
    """
    Function to fetch books from MongoDB database based on query.
    
    The records are stored as follows:
    {
     "title": "The Great Gatsby",
     "author": "F. Scott Fitzgerald",
     "isbn": "978-0-7432-7356-5",
     "genre": "Fiction",
     "publication_year": 1925,
     "quantity_available": 5,
     "quantity_total": 8,
     "location": "A-2-15",
     "publisher": "Scribner",
     "language": "English",
     "status": "available",  # available, checked_out, maintenance
     "added_date": "2024-01-15T10:30:00Z",
     "last_updated": "2024-01-15T10:30:00Z"
    }
    
    Args:
        query: String query for inventory operations. Can be:
               - "all" to get all books
               - "available" to get available books only
               - "genre:Mystery" to get books by genre
               - "author:Stephen King" to get books by author
               - "title:The Great Gatsby" to search by title
               
    Returns:
        Dictionary with 'result' key containing list of matching books
    """
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Library']
        collection = db['Books']  # Fixed collection name to match sampleData.py
        
        # Parse query and build MongoDB filter
        mongo_filter = {}
        
        if query.lower() == "all":
            # Get all books
            mongo_filter = {}
        elif query.lower() == "available":
            # Get only available books
            mongo_filter = {"status": "available"}
        elif ":" in query:
            # Handle specific field queries
            field, value = query.split(":", 1)
            field = field.strip().lower()
            value = value.strip()
            
            if field == "genre":
                mongo_filter = {"genre": {"$regex": value, "$options": "i"}}
            elif field == "author":
                mongo_filter = {"author": {"$regex": value, "$options": "i"}}
            elif field == "title":
                mongo_filter = {"title": {"$regex": value, "$options": "i"}}
            elif field == "status":
                mongo_filter = {"status": value.lower()}
        else:
            # General text search across title, author, and genre
            mongo_filter = {
                "$or": [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"author": {"$regex": query, "$options": "i"}},
                    {"genre": {"$regex": query, "$options": "i"}}
                ]
            }
        
        # Fetch books
        books = list(collection.find(mongo_filter, {'_id': 0}))
        
        logger.info(f"Found {len(books)} books matching query: {query}")
        return {
            "result": books,
            "count": len(books),
            "query": query
        }
            
    except Exception as e:
        logger.error(f"Database operation failed: {str(e)}")
        return {"result": [], "error": str(e), "query": query}
    
    finally:
        if 'client' in locals():
            client.close()

# Recommended book document format in MongoDB:
# {
#     "title": "The Great Gatsby",
#     "author": "F. Scott Fitzgerald",
#     "isbn": "978-0-7432-7356-5",
#     "genre": "Fiction",
#     "publication_year": 1925,
#     "quantity_available": 5,
#     "quantity_total": 8,
#     "location": "A-2-15",
#     "publisher": "Scribner",
#     "language": "English",
#     "status": "available",  # available, checked_out, maintenance
#     "added_date": "2024-01-15T10:30:00Z",
#     "last_updated": "2024-01-15T10:30:00Z"
# }

MODEL = "gemini-2.0-flash"


librarian_agent = Agent(
    model=MODEL,
    name="librarian_agent",
    instruction="You are an agent that can assist with checking and updating inventory of books in a library. You have access to inventory_operations tool which can be used to check the inventory of books in a library. You can also use google_search tool to find information about books. Always provide helpful and accurate information about book availability, locations, and inventory status.",
    tools=[inventory_operations],
)
