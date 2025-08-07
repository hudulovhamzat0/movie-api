🎬 IMDb TSV to JSON Converter (NaN Fixed)

A Python script to convert IMDb TSV (tab-separated values) files into clean JSON format — with special care to fix NaN, inf, and other problematic values. Perfect for preprocessing IMDb datasets for your projects! 🚀
🛠️ Features

    Reads compressed .tsv.gz files directly

    Cleans NaN, inf, and null-like strings into proper JSON null

    Converts numeric columns properly (int, float)

    Supports both normal (in-memory) and streaming (chunked) conversion for large datasets

    Provides data preview for quick inspection

    Validates JSON output after conversion ✅

    Friendly console outputs with emojis for progress feedback 🎉

⚙️ Requirements

    Python 3.7+ 🐍

    pandas

    numpy

Install dependencies:

pip install pandas numpy

📋 Usage

    Set your input and output file paths inside the script or modify before running:

tsv_file = "/path/to/title.basics.tsv.gz"
json_file = "output.json"

    Run the script:

python convert_imdb_tsv.py

    Choose conversion mode:

    1 — Normal conversion (fast, uses more RAM) ⚡

    2 — Streaming conversion (slower, low RAM) 🌊

    The script will preview data, convert, and validate your JSON output.

🧩 How it works

    Reads TSV with gzip compression

    Converts numeric fields carefully

    Recursively cleans NaNs and problematic values

    Dumps pretty-formatted JSON file

    Supports chunked streaming to handle huge files without memory issues

🗂️ Example output

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
  },
  ...
]

💡 Notes

    Adjust max_rows in normal mode for testing smaller data chunks

    Use streaming mode for full datasets > 10 million rows

    Ensure enough disk space for the JSON output

    Customize numeric columns as needed