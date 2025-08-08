# MongoDB JSON Uploader

A Python utility for efficiently uploading large JSON files to MongoDB with batch processing, error handling, and automatic indexing. Specifically designed for IMDb datasets but works with any JSON data.

## Features

- **Batch Processing**: Upload large JSON files in configurable batches for optimal performance
- **Error Handling**: Robust error handling with detailed failure reporting
- **Automatic Indexing**: Creates database indexes for improved query performance
- **Data Validation**: Checks for existing data and provides options to handle duplicates
- **Progress Tracking**: Real-time progress updates during upload process
- **Sample Queries**: Built-in examples to test your uploaded data
- **Connection Testing**: Verifies MongoDB connectivity before operations
- **Flexible Configuration**: Supports local MongoDB and MongoDB Atlas connections

## Prerequisites

- Python 3.7+
- MongoDB 4.0+ (local or Atlas)
- PyMongo library
- JSON file with your data

## Installation

1. **Install required packages**
   ```bash
   pip install pymongo
   ```

2. **Download the uploader**
   ```bash
   # Save the script as mongodb_uploader.py
   wget https://github.com/hudulovhamzat0/movie-api/Convert/convert.py
   ```

3. **Prepare your JSON data**
   - Ensure your JSON file contains an array of objects
   - Place the JSON file in the same directory as the script
   - Rename it to `data.json` or update the script configuration

## Usage

### Basic Usage

1. **Configure the uploader** (edit the script):
   ```python
   # Configuration in main() function
   JSON_FILE = "your_data.json"        # Your JSON file path
   DB_NAME = "imdb_database"           # Database name
   COLLECTION_NAME = "movies"          # Collection name
   BATCH_SIZE = 5000                   # Records per batch
   CONNECTION_STRING = "mongodb://localhost:27017/"
   ```

2. **Run the uploader**
   ```bash
   python mongodb_uploader.py
   ```

### Advanced Configuration

#### MongoDB Connection Options

**Local MongoDB:**
```python
CONNECTION_STRING = "mongodb://localhost:27017/"
```

**MongoDB Atlas:**
```python
CONNECTION_STRING = "mongodb+srv://username:password@cluster.mongodb.net/"
```

**MongoDB with Authentication:**
```python
CONNECTION_STRING = "mongodb://username:password@localhost:27017/"
```

#### Batch Size Recommendations

- **Small datasets** (< 100K records): `1000-5000`
- **Medium datasets** (100K-1M records): `5000-10000`
- **Large datasets** (> 1M records): `10000-50000`

## JSON Data Format

The uploader expects JSON files with this structure:

```json
[
  {
    "field1": "value1",
    "field2": "value2",
    "field3": 123
  },
  {
    "field1": "value3",
    "field2": "value4",
    "field3": 456
  }
]
```

### IMDb Dataset Examples

**For title.basics.tsv converted to JSON:**
```json
[
  {
    "tconst": "tt0000001",
    "titleType": "short",
    "primaryTitle": "Carmencita",
    "originalTitle": "Carmencita",
    "isAdult": 0,
    "startYear": 1894,
    "endYear": null,
    "runtimeMinutes": 1,
    "genres": "Documentary,Short"
  }
]
```

**For name.basics.tsv converted to JSON:**
```json
[
  {
    "nconst": "nm0000001",
    "primaryName": "Fred Astaire",
    "birthYear": 1899,
    "deathYear": 1987,
    "primaryProfession": "soundtrack,actor,miscellaneous",
    "knownForTitles": "tt0050419,tt0053137,tt0027125,tt0072308"
  }
]
```

## Class Reference

### MongoDBUploader

#### Constructor
```python
uploader = MongoDBUploader(connection_string=None, database_name="imdb_database")
```

**Parameters:**
- `connection_string`: MongoDB connection string (default: localhost)
- `database_name`: Target database name

#### Methods

##### upload_json_file()
```python
inserted_count, failed_inserts = uploader.upload_json_file(
    json_file_path="data.json",
    collection_name="movies",
    batch_size=1000
)
```
Uploads JSON file to MongoDB collection.

##### create_indexes()
```python
uploader.create_indexes(collection_name, ["field1", "field2"])
```
Creates database indexes for improved query performance.

##### query_examples()
```python
uploader.query_examples(collection_name)
```
Runs sample queries and displays collection statistics.

## Performance Optimization

### Recommended Indexes

**For IMDb title data:**
```python
title_indexes = ["tconst", "titleType", "startYear", "genres", "primaryTitle"]
```

**For IMDb name data:**
```python
name_indexes = ["nconst", "primaryName", "birthYear", "primaryProfession"]
```

### Memory Management

- Large files are processed in batches to prevent memory issues
- Failed inserts are tracked separately to avoid memory leaks
- Connections are properly closed after operations

## Error Handling

The uploader handles various error scenarios:

- **Connection failures**: Validates MongoDB connectivity
- **File not found**: Checks JSON file existence
- **Invalid JSON**: Catches JSON parsing errors
- **Duplicate data**: Options to handle existing collections
- **Bulk write errors**: Continues processing and reports failures
- **Index creation failures**: Non-blocking index errors

## Example Output

```
🎬 MongoDB JSON Uploader
==================================================
✅ MongoDB connection successful!
📊 Database: imdb_database
📂 Reading JSON file: data.json
📊 Total records: 50000
⚠️  Collection already has 25000 records!
Type 'y' to delete existing data: y
🗑️  Existing data deleted!
🚀 Uploading data in batches of 5000...
✅ Batch 1: Inserted 5000 records
✅ Batch 2: Inserted 5000 records
...
==================================================
🎉 Upload completed!
📊 Total successful: 50000
❌ Failed: 0
🏷️  Collection: movies
📈 Total documents in collection: 50000

🔍 Creating indexes...
✅ Index created: tconst
✅ Index created: titleType
...
```

## Sample Queries

After upload, the script provides sample queries:

```python
# Count total documents
total = collection.count_documents({})

# Find recent movies
recent_movies = collection.find(
    {"startYear": {"$gte": 2020}, "titleType": "movie"}
).limit(10)

# Search by genre
action_movies = collection.find(
    {"genres": {"$regex": "Action", "$options": "i"}}
)

# Find living people (for name data)
alive_people = collection.find({"deathYear": None})
```

## Converting TSV to JSON

If you have IMDb TSV files, convert them to JSON first:

### Using Python pandas:
```python
import pandas as pd
import json

# Read TSV file
df = pd.read_csv('title.basics.tsv', sep='\t', na_values='\\N')

# Convert to JSON
df.to_json('title_basics.json', orient='records', indent=2)
```

### Using online converters:
- ConvertCSV.com
- csvjson.com

## Troubleshooting

### Common Issues

**"No module named 'pymongo'"**
```bash
pip install pymongo
```

**"JSON file not found"**
- Check file path and name
- Ensure file is in the script directory

**"Connection refused"**
- Verify MongoDB is running
- Check connection string
- Verify firewall/network settings

**"Out of memory"**
- Reduce batch size
- Check available system memory
- Process file in smaller chunks

### Performance Issues

**Slow uploads:**
- Increase batch size (try 10000-50000)
- Ensure MongoDB has sufficient resources
- Check network connection for remote MongoDB

**High memory usage:**
- Decrease batch size
- Close other applications
- Use a machine with more RAM

## Integration with Flask App

This uploader works perfectly with the IMDb Flask search application:

1. **Upload your data** using this script
2. **Configure Flask app** to use the same database/collection
3. **Create search indexes** for optimal performance
4. **Test the web interface** with uploaded data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Check the troubleshooting section
- Review MongoDB documentation
- Create an issue in the repository

---

**Note**: This utility is designed for IMDb datasets but can be adapted for any JSON data upload to MongoDB. Always backup your database before running bulk operations.