import json
import pymongo
from pymongo import MongoClient
from datetime import datetime
import os
from typing import Optional

class MongoDBUploader:
    def __init__(self, connection_string: str = None, database_name: str = "imdb_database"):
        """
        MongoDB uploader initialization
        
        Args:
            connection_string: MongoDB connection string (default: localhost)
            database_name: Database name
        """
        if connection_string is None:
            # Default local MongoDB connection
            connection_string = "mongodb://localhost:27017/"
        
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client[database_name]
            
            # Test connection
            self.client.admin.command('ping')
            print(f"✅ MongoDB connection successful!")
            print(f"📊 Database: {database_name}")
            
        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            raise
    
    def upload_json_file(self, json_file_path: str, collection_name: str, batch_size: int = 1000):
        """
        Upload JSON file to MongoDB
        
        Args:
            json_file_path: JSON file path
            collection_name: MongoDB collection name
            batch_size: Batch size (for performance)
        """
        try:
            print(f"📂 Reading JSON file: {json_file_path}")
            
            # Read JSON file
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📊 Total records: {len(data)}")
            
            # Get or create collection
            collection = self.db[collection_name]
            
            # If collection exists, clear it (optional)
            existing_count = collection.count_documents({})
            if existing_count > 0:
                print(f"⚠️  Collection already has {existing_count} records!")
                choice = input("Type 'y' to delete existing data: ").strip().lower()
                if choice == 'y':
                    collection.delete_many({})
                    print("🗑️  Existing data deleted!")
            
            # Upload data in batches
            print(f"🚀 Uploading data in batches of {batch_size}...")
            
            total_inserted = 0
            failed_inserts = []
            
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                
                try:
                    # Insert batch into MongoDB
                    result = collection.insert_many(batch, ordered=False)
                    total_inserted += len(result.inserted_ids)
                    
                    print(f"✅ Batch {i//batch_size + 1}: Inserted {len(batch)} records")
                    
                except pymongo.errors.BulkWriteError as e:
                    # Some records might fail
                    successful = len(batch) - len(e.details['writeErrors'])
                    total_inserted += successful
                    failed_inserts.extend(e.details['writeErrors'])
                    
                    print(f"⚠️  Batch {i//batch_size + 1}: Inserted {successful}/{len(batch)} records")
            
            # Report results
            print("\n" + "="*50)
            print(f"🎉 Upload completed!")
            print(f"📊 Total successful: {total_inserted}")
            print(f"❌ Failed: {len(failed_inserts)}")
            print(f"🏷️  Collection: {collection_name}")
            
            # Collection stats
            final_count = collection.count_documents({})
            print(f"📈 Total documents in collection: {final_count}")
            
            if failed_inserts:
                print(f"\n⚠️  Failed inserts:")
                for error in failed_inserts[:5]:  # Show first 5 errors
                    print(f"  - Index {error['index']}: {error['errmsg']}")
                if len(failed_inserts) > 5:
                    print(f"  ... and {len(failed_inserts) - 5} more errors")
            
            return total_inserted, failed_inserts
            
        except Exception as e:
            print(f"❌ Upload error: {e}")
            import traceback
            traceback.print_exc()
            return 0, []
    
    def create_indexes(self, collection_name: str, index_fields: list):
        """
        Create indexes for performance
        
        Args:
            collection_name: Collection name
            index_fields: Fields to create indexes on
        """
        try:
            collection = self.db[collection_name]
            
            print(f"🔍 Creating indexes...")
            
            for field in index_fields:
                try:
                    collection.create_index(field)
                    print(f"✅ Index created: {field}")
                except Exception as e:
                    print(f"⚠️  Could not create index ({field}): {e}")
            
            # List existing indexes
            indexes = list(collection.list_indexes())
            print(f"\n📋 Existing indexes:")
            for idx in indexes:
                print(f"  - {idx['name']}: {idx.get('key', {})}")
                
        except Exception as e:
            print(f"❌ Index creation error: {e}")
    
    def query_examples(self, collection_name: str):
        """
        Sample queries
        """
        try:
            collection = self.db[collection_name]
            
            print(f"\n🔍 Sample queries ({collection_name}):")
            print("-" * 40)
            
            # Total documents
            total = collection.count_documents({})
            print(f"📊 Total documents: {total}")
            
            # First document
            first_doc = collection.find_one()
            if first_doc:
                print(f"📄 Sample first document:")
                # Remove ObjectId (not JSON serializable)
                first_doc.pop('_id', None)
                print(json.dumps(first_doc, indent=2, ensure_ascii=False))
            
            # Analyze fields
            if first_doc:
                print(f"\n📝 Available fields:")
                for field in first_doc.keys():
                    print(f"  - {field}")
            
            # Examples for title.basics
            if 'tconst' in (first_doc or {}):
                print(f"\n🎬 Movie samples:")
                
                # Filter by year
                recent_movies = list(collection.find(
                    {"startYear": {"$gte": 2020}, "titleType": "movie"}
                ).limit(3))
                
                print(f"2020+ movies found: {len(recent_movies)}")
                
                # Filter by genre
                action_movies = collection.count_documents(
                    {"genres": {"$regex": "Action", "$options": "i"}}
                )
                print(f"Action movies count: {action_movies}")
            
            # Examples for name.basics
            if 'nconst' in (first_doc or {}):
                print(f"\n🎭 Name samples:")
                
                # Living people
                alive_people = collection.count_documents({"deathYear": None})
                print(f"Living people: {alive_people}")
                
                # Specific profession
                directors = collection.count_documents(
                    {"primaryProfession": {"$regex": "director", "$options": "i"}}
                )
                print(f"Directors count: {directors}")
                
        except Exception as e:
            print(f"❌ Query error: {e}")
    
    def close(self):
        """
        Close MongoDB connection
        """
        if self.client:
            self.client.close()
            print("🔐 MongoDB connection closed")

# Main program
def main():
    print("🎬 MongoDB JSON Uploader")
    print("=" * 50)
    
    # Configuration
    JSON_FILE = "data.json"  # JSON file path
    DB_NAME = "imdb_database"            # Database name
    COLLECTION_NAME = "movies"           # Collection name
    BATCH_SIZE = 5000                   # Batch size
    
    # MongoDB connection string options:
    # Local: "mongodb://localhost:27017/"
    # Atlas: "mongodb+srv://username:password@cluster.mongodb.net/"
    CONNECTION_STRING = "mongodb://localhost:27017/"
    
    try:
        # Connect to MongoDB
        uploader = MongoDBUploader(CONNECTION_STRING, DB_NAME)
        
        # Check if JSON file exists
        if not os.path.exists(JSON_FILE):
            print(f"❌ JSON file not found: {JSON_FILE}")
            print("Please check the file path!")
            return
        
        # Upload process
        inserted_count, failed = uploader.upload_json_file(
            json_file_path=JSON_FILE,
            collection_name=COLLECTION_NAME,
            batch_size=BATCH_SIZE
        )
        
        if inserted_count > 0:
            # Create indexes for performance
            print(f"\n🔍 Creating indexes...")
            
            # Indexes for title.basics
            title_indexes = ["tconst", "titleType", "startYear", "genres"]
            # Indexes for name.basics  
            name_indexes = ["nconst", "primaryName", "birthYear", "primaryProfession"]
            
            # Create indexes based on type
            uploader.create_indexes(COLLECTION_NAME, title_indexes)
            
            # Show sample queries
            uploader.query_examples(COLLECTION_NAME)
        
        # Close connection
        uploader.close()
        
    except Exception as e:
        print(f"❌ Program error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
