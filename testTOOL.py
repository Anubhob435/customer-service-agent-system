import logging
from datetime import datetime
from pymongo import MongoClient
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
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


def test_inventory_operations():
    """Test function to verify inventory_operations works correctly"""
    print("🧪 Testing inventory_operations function...")
    print("=" * 60)
    
    # Test cases
    test_queries = [
        "all",
        "available", 
        "genre:Mystery",
        "genre:Fiction",
        "author:Andy Weir",
        "author:Orwell",
        "title:Gatsby",
        "title:1984",
        "status:available",
        "status:checked_out",
        "Atomic",  # General search
        "Mystery"  # General search
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📚 Test {i}: Query = '{query}'")
        print("-" * 40)
        
        try:
            result = inventory_operations(query)
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Success: Found {result['count']} books")
                
                # Show first few results for verification
                if result['result'] and len(result['result']) > 0:
                    print("📖 Sample results:")
                    for j, book in enumerate(result['result'][:3], 1):  # Show first 3 books
                        print(f"   {j}. {book.get('title', 'N/A')} by {book.get('author', 'N/A')}")
                        print(f"      Genre: {book.get('genre', 'N/A')}, Status: {book.get('status', 'N/A')}")
                        if j < len(result['result']) and j < 3:
                            print()
                    
                    if len(result['result']) > 3:
                        print(f"   ... and {len(result['result']) - 3} more books")
                else:
                    print("📖 No books found matching this query")
                    
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🏁 Testing completed!")


def test_database_connection():
    """Test if MongoDB connection is working"""
    print("🔌 Testing MongoDB connection...")
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Library']
        collection = db['Books']
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Get collection stats
        total_docs = collection.count_documents({})
        print(f"📊 Total books in collection: {total_docs}")
        
        if total_docs > 0:
            # Sample document
            sample_doc = collection.find_one({}, {'_id': 0})
            print("📚 Sample document structure:")
            for key, value in list(sample_doc.items())[:5]:  # Show first 5 fields
                print(f"   {key}: {value}")
            if len(sample_doc) > 5:
                print(f"   ... and {len(sample_doc) - 5} more fields")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        print("💡 Make sure MongoDB is running on localhost:27017")
        print("💡 Run 'python sampleData.py' to populate the database first")
        return False


def main():
    """Main test function"""
    print("🚀 Starting inventory_operations function tests")
    print("=" * 60)
    
    # First test database connection
    if test_database_connection():
        print("\n")
        # If connection works, run the function tests
        test_inventory_operations()
    else:
        print("\n❌ Cannot run function tests without database connection")


if __name__ == "__main__":
    main()
