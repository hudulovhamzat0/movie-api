📦 MongoDB JSON Uploader

A Python utility to upload large JSON files into MongoDB collections efficiently with batching and indexing support. Designed to work well with IMDb JSON datasets or similar large JSON data.
🚀 Features

    Connects to local or remote MongoDB instance

    Uploads JSON data in batches for performance and stability

    Optionally clears existing collection data before upload

    Creates indexes on specified fields for faster queries

    Provides sample queries to explore the uploaded data

    Handles bulk write errors and reports failures

    Simple CLI interaction for confirmation prompts

🛠️ Requirements

    Python 3.7+

    pymongo package

Install dependencies via:

pip install pymongo

Make sure MongoDB is running and accessible.
⚙️ Usage

    Configure the constants in main():

        JSON_FILE: Path to your JSON data file (e.g., data.json)

        DB_NAME: Target MongoDB database name

        COLLECTION_NAME: Target collection name

        BATCH_SIZE: Number of documents per upload batch

        CONNECTION_STRING: MongoDB connection URI

    Run the script:

python mongodb_uploader.py

    If the target collection has existing data, you will be prompted whether to delete it before uploading new data.

    After upload, indexes will be created on commonly queried fields to optimize performance.

    Sample queries and collection stats will be printed for quick verification.

🧑‍💻 Example Output

🎬 MongoDB JSON Uploader
==================================================
✅ MongoDB connection successful!
📊 Database: imdb_database
📂 Reading JSON file: data.json
📊 Total records: 120000
⚠️  Collection already has 50000 records!
Type 'y' to delete existing data: y
🗑️  Existing data deleted!
🚀 Uploading data in batches of 5000...
✅ Batch 1: Inserted 5000 records
✅ Batch 2: Inserted 5000 records
...
🎉 Upload completed!
📊 Total successful: 120000
❌ Failed: 0
🏷️  Collection: movies
📈 Total documents in collection: 120000

🔍 Creating indexes...
✅ Index created: tconst
✅ Index created: titleType
...

🔍 Sample queries (movies):
----------------------------------------
📊 Total documents: 120000
📄 Sample first document:
{
  "tconst": "tt1234567",
  "titleType": "movie",
  ...
}
📝 Available fields:
  - tconst
  - titleType
  - primaryTitle
  - ...

⚠️ Notes

    Ensure your JSON file contains a list of documents compatible with MongoDB (dict objects).

    Adjust batch_size according to your system memory and network speed.

    Index creation fields can be customized in the script to match your dataset schema.

🤝 Contribution

Feel free to open issues or pull requests to improve this uploader tool!
📜 License

MIT License
