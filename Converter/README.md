# IMDb TSV to JSON Converter

A robust Python utility for converting IMDb TSV (Tab-Separated Values) files to clean JSON format. Specifically designed to handle IMDb dataset peculiarities like `\N` null values, mixed data types, and large file sizes with memory-efficient streaming support.

## Features

- **Clean Data Processing**: Handles `\N`, NaN, and other problematic values in IMDb datasets
- **Smart Type Detection**: Automatically converts numeric columns while preserving data integrity
- **Memory Efficient**: Two processing modes - normal and streaming for large files
- **Data Validation**: Built-in JSON validation and preview functionality
- **Progress Tracking**: Real-time progress updates during conversion
- **Error Handling**: Comprehensive error handling with detailed error messages
- **IMDb Optimized**: Specifically designed for IMDb title.basics and name.basics datasets
- **Gzip Support**: Direct processing of compressed `.tsv.gz` files

## Prerequisites

- Python 3.7+
- pandas
- numpy
- IMDb TSV files (compressed or uncompressed)

## Installation

1. **Install required packages**
   ```bash
   pip install pandas numpy
   ```

2. **Download the converter**
   ```bash
   # Save the script as tsv_converter.py
   wget https://github.com/hudulovhamzat0/movie-api/Converter/converter.py
   ```

## Usage

### Quick Start

1. **Update file paths** in the script:
   ```python
   tsv_file = "path/to/your/title.basics.tsv.gz"
   json_file = "output_data.json"
   ```

2. **Run the converter**
   ```bash
   python tsv_converter.py
   ```

3. **Choose conversion mode**:
   - **Option 1**: Normal conversion (faster, more RAM usage)
   - **Option 2**: Streaming conversion (slower, memory-efficient)

### Advanced Usage

#### Preview Data Before Conversion
```python
from tsv_converter import preview_data

# Preview first 5 rows
preview_data("title.basics.tsv.gz", num_rows=5)
```

#### Normal Conversion (Fast)
```python
from tsv_converter import convert_imdb_tsv_to_json

result = convert_imdb_tsv_to_json(
    tsv_file_path="title.basics.tsv.gz",
    output_json_path="movies.json",
    max_rows=50000  # Limit for testing, remove for full conversion
)
```

#### Streaming Conversion (Memory-Efficient)
```python
from tsv_converter import convert_large_tsv_streaming

convert_large_tsv_streaming(
    tsv_file_path="title.basics.tsv.gz",
    output_json_path="movies.json",
    chunk_size=10000  # Process in chunks
)
```

## Supported IMDb Datasets

### title.basics.tsv.gz
Contains movie and TV show information:
- `tconst` - Title identifier
- `titleType` - Type (movie, short, tvSeries, etc.)
- `primaryTitle` - Primary title
- `originalTitle` - Original title
- `isAdult` - Adult content flag (0/1)
- `startYear` - Release year
- `endYear` - End year (for series)
- `runtimeMinutes` - Runtime in minutes
- `genres` - Comma-separated genres

### name.basics.tsv.gz
Contains people information:
- `nconst` - Name identifier
- `primaryName` - Person's name
- `birthYear` - Birth year
- `deathYear` - Death year
- `primaryProfession` - Comma-separated professions
- `knownForTitles` - Comma-separated title identifiers

## Data Cleaning Features

### Null Value Handling
The converter handles various null representations:
- `\N` (IMDb standard null)
- `NaN`, `nan`, `NULL`, `null`
- Empty strings
- Actual NaN/inf values from pandas

### Type Conversion
- **Numeric fields** are converted to integers/floats
- **String fields** preserve original text
- **Invalid numeric values** become `null` in JSON
- **Empty/null values** become `null` in JSON

### Before and After Example

**Original TSV:**
```
tconst	titleType	primaryTitle	startYear	runtimeMinutes
tt0000001	short	Carmencita	1894	1
tt0000002	short	\N	\N	\N
```

**Converted JSON:**
```json
[
  {
    "tconst": "tt0000001",
    "titleType": "short",
    "primaryTitle": "Carmencita",
    "startYear": 1894,
    "runtimeMinutes": 1
  },
  {
    "tconst": "tt0000002",
    "titleType": "short",
    "primaryTitle": null,
    "startYear": null,
    "runtimeMinutes": null
  }
]
```

## Function Reference

### convert_imdb_tsv_to_json()
Main conversion function for normal processing.

```python
convert_imdb_tsv_to_json(
    tsv_file_path: str,          # Input TSV file path
    output_json_path: str,       # Output JSON file path
    max_rows: Optional[int] = None  # Limit rows (for testing)
) -> List[dict]
```

**Returns**: List of dictionaries (JSON data)

### convert_large_tsv_streaming()
Memory-efficient streaming conversion for large files.

```python
convert_large_tsv_streaming(
    tsv_file_path: str,     # Input TSV file path
    output_json_path: str,  # Output JSON file path
    chunk_size: int = 10000 # Rows per chunk
)
```

### preview_data()
Preview TSV data before conversion.

```python
preview_data(
    tsv_file_path: str,  # Input TSV file path
    num_rows: int = 5    # Number of rows to preview
) -> pandas.DataFrame
```

### clean_nan_values()
Utility function to clean problematic values.

```python
clean_nan_values(obj) -> Any
```

## Performance Guidelines

### File Size Recommendations

| File Size | Recommended Mode | Chunk Size | Expected Time |
|-----------|------------------|------------|---------------|
| < 100 MB  | Normal          | N/A        | < 1 minute    |
| 100-500 MB| Normal          | N/A        | 1-5 minutes   |
| 500 MB-2 GB| Streaming      | 10,000     | 5-20 minutes  |
| > 2 GB    | Streaming       | 5,000      | 20+ minutes   |

### Memory Usage

- **Normal mode**: ~3x file size in RAM
- **Streaming mode**: ~50 MB RAM regardless of file size

## Output Validation

The converter includes built-in validation:

1. **JSON Syntax Check**: Verifies output is valid JSON
2. **Data Integrity Check**: Ensures no data corruption
3. **Type Validation**: Confirms proper type conversions
4. **Sample Output**: Shows converted record examples

## Example Output

```
🎬 IMDb TSV to JSON Converter (NaN Fixed)
==================================================
👀 Veri önizlemesi yapılıyor...
📋 Veri önizlemesi:
============================================================
     tconst titleType    primaryTitle  startYear
0  tt0000001     short      Carmencita       1894
1  tt0000002     short  Le clown et... 1896

📊 Sütun bilgileri:
Data columns (total 9 columns):
...

Dönüştürme seçenekleri:
1. Normal conversion (hızlı, daha fazla RAM)
2. Streaming conversion (yavaş, az RAM)
Seçiminiz (1 veya 2): 1

Dosya okunuyor: title.basics.tsv.gz
Toplam 50000 kayıt okundu
Sütunlar: ['tconst', 'titleType', 'primaryTitle', ...]
Veri temizliği yapılıyor...
JSON'a dönüştürülüyor...
JSON dosyası yazılıyor...
✅ Başarıyla dönüştürüldü: data.json
📊 JSON dosyası 50000 kayıt içeriyor
🔍 JSON validation testi...
✅ JSON dosyası geçerli!
```

## Integration with MongoDB Uploader

This converter works perfectly with the MongoDB uploader:

1. **Convert TSV to JSON** using this script
2. **Upload JSON to MongoDB** using the MongoDB uploader
3. **Use in Flask app** for search functionality

### Complete Workflow
```bash
# Step 1: Convert TSV to JSON
python tsv_converter.py

# Step 2: Upload to MongoDB  
python mongodb_uploader.py

# Step 3: Run Flask app
python app.py
```

## Troubleshooting

### Common Issues

**"No module named 'pandas'"**
```bash
pip install pandas numpy
```

**"Memory Error"**
- Use streaming conversion mode
- Reduce chunk size
- Close other applications

**"Invalid JSON output"**
- Check source TSV file encoding
- Verify no corrupted data in source
- Try smaller test conversion first

**"File not found"**
- Check file path and permissions
- Verify gzip file is not corrupted
- Use absolute file paths

### Performance Issues

**Slow conversion:**
- Use normal mode for smaller files
- Increase chunk size for streaming mode
- Use SSD storage for better I/O

**High memory usage:**
- Switch to streaming mode
- Reduce max_rows for testing
- Close unnecessary applications

## Configuration

### Customizing for Other Datasets

To adapt for non-IMDb TSV files:

1. **Update numeric columns**:
   ```python
   # Modify these lists based on your data
   numeric_columns = ['your_numeric_column1', 'your_numeric_column2']
   ```

2. **Adjust null value handling**:
   ```python
   # Add your null representations
   na_values=['\\N', 'NULL', 'missing', 'your_null_value']
   ```

3. **Modify data types**:
   ```python
   # Add custom type conversions in the processing loop
   ```

## Best Practices

1. **Always preview data first** using `preview_data()`
2. **Start with small test files** (use `max_rows` parameter)
3. **Use streaming mode for files > 500MB**
4. **Validate JSON output** before uploading to database
5. **Keep original TSV files** as backups
6. **Monitor memory usage** during conversion

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Check the troubleshooting section
- Review pandas documentation for TSV issues
- Create an issue in the repository

---

**Note**: This converter is optimized for IMDb datasets but can be adapted for any TSV to JSON conversion needs. Always test with a small sample before processing large files.