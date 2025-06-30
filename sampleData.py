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

from pymongo import MongoClient
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongoDB_Host = "localhost:27017 / Library / shelf / Books is the collection name"

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "Library"
COLLECTION_NAME = "Books"

# Sample book data for the collection
sample_books = [
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
        "status": "available",
        "added_date": "2024-01-15T10:30:00Z",
        "last_updated": "2024-01-15T10:30:00Z"
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "isbn": "978-0-06-112008-4",
        "genre": "Fiction",
        "publication_year": 1960,
        "quantity_available": 3,
        "quantity_total": 6,
        "location": "A-3-22",
        "publisher": "J.B. Lippincott & Co.",
        "language": "English",
        "status": "available",
        "added_date": "2024-01-20T14:15:00Z",
        "last_updated": "2024-06-15T09:20:00Z"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "978-0-452-28423-4",
        "genre": "Science Fiction",
        "publication_year": 1949,
        "quantity_available": 7,
        "quantity_total": 10,
        "location": "B-1-08",
        "publisher": "Secker & Warburg",
        "language": "English",
        "status": "available",
        "added_date": "2024-02-01T11:45:00Z",
        "last_updated": "2024-06-28T16:30:00Z"
    },
    {
        "title": "The Thursday Murder Club",
        "author": "Richard Osman",
        "isbn": "978-0-525-63489-9",
        "genre": "Mystery",
        "publication_year": 2020,
        "quantity_available": 2,
        "quantity_total": 4,
        "location": "C-2-11",
        "publisher": "Viking",
        "language": "English",
        "status": "available",
        "added_date": "2024-03-10T08:20:00Z",
        "last_updated": "2024-06-25T13:15:00Z"
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "isbn": "978-0-399-59050-4",
        "genre": "Memoir",
        "publication_year": 2018,
        "quantity_available": 4,
        "quantity_total": 6,
        "location": "D-1-33",
        "publisher": "Random House",
        "language": "English",
        "status": "available",
        "added_date": "2024-02-15T12:10:00Z",
        "last_updated": "2024-06-20T10:45:00Z"
    },
    {
        "title": "The Seven Husbands of Evelyn Hugo",
        "author": "Taylor Jenkins Reid",
        "isbn": "978-1-5011-3981-9",
        "genre": "Fiction",
        "publication_year": 2017,
        "quantity_available": 6,
        "quantity_total": 8,
        "location": "A-4-18",
        "publisher": "Atria Books",
        "language": "English",
        "status": "available",
        "added_date": "2024-01-25T15:30:00Z",
        "last_updated": "2024-06-22T14:20:00Z"
    },
    {
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "isbn": "978-0-593-13520-1",
        "genre": "Science Fiction",
        "publication_year": 2021,
        "quantity_available": 3,
        "quantity_total": 5,
        "location": "B-3-27",
        "publisher": "Ballantine Books",
        "language": "English",
        "status": "available",
        "added_date": "2024-03-05T09:15:00Z",
        "last_updated": "2024-06-18T11:30:00Z"
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "isbn": "978-0-7352-1129-2",
        "genre": "Self-Help",
        "publication_year": 2018,
        "quantity_available": 8,
        "quantity_total": 10,
        "location": "E-1-05",
        "publisher": "Avery",
        "language": "English",
        "status": "available",
        "added_date": "2024-01-30T13:40:00Z",
        "last_updated": "2024-06-29T08:50:00Z"
    },
    {
        "title": "Gone Girl",
        "author": "Gillian Flynn",
        "isbn": "978-0-307-58836-4",
        "genre": "Mystery",
        "publication_year": 2012,
        "quantity_available": 1,
        "quantity_total": 4,
        "location": "C-1-14",
        "publisher": "Crown Publishers",
        "language": "English",
        "status": "available",
        "added_date": "2024-02-20T16:25:00Z",
        "last_updated": "2024-06-26T15:10:00Z"
    },
    {
        "title": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "isbn": "978-0-307-45454-1",
        "genre": "Mystery",
        "publication_year": 2005,
        "quantity_available": 2,
        "quantity_total": 5,
        "location": "C-3-19",
        "publisher": "Norstedts Förlag",
        "language": "English",
        "status": "available",
        "added_date": "2024-02-25T10:15:00Z",
        "last_updated": "2024-06-24T12:35:00Z"
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "978-0-441-17271-9",
        "genre": "Science Fiction",
        "publication_year": 1965,
        "quantity_available": 4,
        "quantity_total": 7,
        "location": "B-2-12",
        "publisher": "Chilton Books",
        "language": "English",
        "status": "available",
        "added_date": "2024-01-10T14:50:00Z",
        "last_updated": "2024-06-27T09:40:00Z"
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "isbn": "978-0-553-41802-6",
        "genre": "Science Fiction",
        "publication_year": 2011,
        "quantity_available": 0,
        "quantity_total": 3,
        "location": "B-3-28",
        "publisher": "Crown Publishers",
        "language": "English",
        "status": "checked_out",
        "added_date": "2024-03-01T11:20:00Z",
        "last_updated": "2024-06-30T07:15:00Z"
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "isbn": "978-1-250-30170-7",
        "genre": "Mystery",
        "publication_year": 2019,
        "quantity_available": 3,
        "quantity_total": 4,
        "location": "C-2-16",
        "publisher": "Celadon Books",
        "language": "English",
        "status": "available",
        "added_date": "2024-02-10T12:30:00Z",
        "last_updated": "2024-06-23T14:45:00Z"
    },
    {
        "title": "Where the Crawdads Sing",
        "author": "Delia Owens",
        "isbn": "978-0-7352-1909-0",
        "genre": "Fiction",
        "publication_year": 2018,
        "quantity_available": 1,
        "quantity_total": 6,
        "location": "A-1-07",
        "publisher": "G.P. Putnam's Sons",
        "language": "English",
        "status": "maintenance",
        "added_date": "2024-01-18T09:45:00Z",
        "last_updated": "2024-06-29T16:20:00Z"
    },
    {
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "isbn": "978-0-525-55947-3",
        "genre": "Fiction",
        "publication_year": 2020,
        "quantity_available": 5,
        "quantity_total": 6,
        "location": "A-3-24",
        "publisher": "Viking",
        "language": "English",
        "status": "available",
        "added_date": "2024-03-15T13:25:00Z",
        "last_updated": "2024-06-21T11:55:00Z"
    }
]

# Collection statistics
total_books = len(sample_books)
available_books = len([book for book in sample_books if book["status"] == "available"])
checked_out_books = len([book for book in sample_books if book["status"] == "checked_out"])
maintenance_books = len([book for book in sample_books if book["status"] == "maintenance"])

print(f"Total books in collection: {total_books}")
print(f"Available books: {available_books}")
print(f"Checked out books: {checked_out_books}")
print(f"Books in maintenance: {maintenance_books}")

# Genre distribution
genres = {}
for book in sample_books:
    genre = book["genre"]
    genres[genre] = genres.get(genre, 0) + 1

print("\nGenre distribution:")
for genre, count in genres.items():
    print(f"  {genre}: {count} books")

# MongoDB operations
def connect_to_mongodb():
    """Connect to MongoDB and return the collection object"""
    try:
        client = MongoClient(MONGO_URI)
        # Test the connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        return collection, client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return None, None

def insert_books_to_mongodb(books_data):
    """Insert sample books into MongoDB collection"""
    collection, client = connect_to_mongodb()
    
    if collection is None:
        logger.error("Cannot insert books - MongoDB connection failed")
        return False
    
    try:
        # Clear existing data (optional - remove this if you want to keep existing books)
        existing_count = collection.count_documents({})
        if existing_count > 0:
            logger.info(f"Found {existing_count} existing books in collection")
            choice = input("Do you want to clear existing books and insert fresh data? (y/n): ").lower()
            if choice == 'y':
                collection.delete_many({})
                logger.info("Cleared existing books from collection")
        
        # Insert new books
        result = collection.insert_many(books_data)
        logger.info(f"Successfully inserted {len(result.inserted_ids)} books into MongoDB")
        
        # Verify insertion
        total_count = collection.count_documents({})
        logger.info(f"Total books in collection: {total_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to insert books: {e}")
        return False
    finally:
        if client:
            client.close()
            logger.info("MongoDB connection closed")

def query_books_examples(collection):
    """Example queries to demonstrate MongoDB operations"""
    try:
        # Find books by genre
        mystery_books = list(collection.find({"genre": "Mystery"}))
        print(f"\nMystery books found: {len(mystery_books)}")
        
        # Find available books
        available_books = list(collection.find({"status": "available"}))
        print(f"Available books: {len(available_books)}")
        
        # Find books by author
        orwell_books = list(collection.find({"author": {"$regex": "Orwell", "$options": "i"}}))
        print(f"Books by Orwell: {len(orwell_books)}")
        
        # Find recent books (published after 2015)
        recent_books = list(collection.find({"publication_year": {"$gt": 2015}}))
        print(f"Books published after 2015: {len(recent_books)}")
        
    except Exception as e:
        logger.error(f"Query examples failed: {e}")

def main():
    """Main function to execute MongoDB operations"""
    print("=" * 50)
    print("MONGODB BOOK STORAGE OPERATION")
    print("=" * 50)
    
    # Insert books into MongoDB
    if insert_books_to_mongodb(sample_books):
        print("\n✅ Books successfully stored in MongoDB!")
        
        # Connect again for queries
        collection, client = connect_to_mongodb()
        if collection is not None:
            print("\n📊 Running example queries...")
            query_books_examples(collection)
            client.close()
    else:
        print("\n❌ Failed to store books in MongoDB")

if __name__ == "__main__":
    main()

