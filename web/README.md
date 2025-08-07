🎬 IMDb Search App

A simple Flask web app for live searching and autocomplete suggestions on movies, series, and actors — powered by MongoDB. Clean, modern, and responsive UI with a dark red-black theme. ❤️‍🔥
✨ Features

    🔍 Live search on titles, names, genres, and professions

    💡 Autocomplete suggestions as you type

    🗄️ MongoDB integration with flexible schema support

    ⚡ Fast API endpoints for search, suggestions & stats

    🖤 Stylish dark theme with red accents

🛠️ Requirements

    Python 3.7+ 🐍

    Flask

    pymongo

    MongoDB (local or remote)

🚀 Installation

    Clone the repo:

git clone https://github.com/yourusername/imdb-search.git
cd imdb-search

(Optional) Create & activate virtual environment:

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

Install dependencies:

    pip install -r requirements.txt

    Make sure MongoDB is running on mongodb://localhost:27017/ or update the connection string in app.py.

    Populate your MongoDB database & collection with IMDb-like data.

🏃 Usage

Start the Flask server:

python app.py

Open your browser at: http://localhost:5000 🔥
📡 API Endpoints
GET /api/search?q=<query>

    Search movies, series, actors, etc. (min 2 chars)

    Returns top 10 matches

    Example response:

{
  "results": [
    {
      "_id": "60c72b2f9e7e2a001f4a9b9e",
      "primaryTitle": "Inception",
      "genres": ["Action", "Sci-Fi"]
    }
  ],
  "total": 1,
  "query": "Inception"
}

GET /api/suggestions?q=<query>

    Autocomplete suggestions (top 5)

    Example:

{
  "suggestions": ["Inception", "Interstellar", "Inside Out"]
}

GET /api/stats

    Shows DB stats like total documents, collection & DB names.

📁 Project Structure

.
├── app.py            # Flask backend
├── requirements.txt  # Python deps
├── templates/
│   └── index.html    # Main UI template
├── static/
│   ├── css/
│   │   └── index.css # Stylesheet
│   └── js/
│       └── main.js   # Frontend logic
└── README.md         # You’re reading it! 😄

📜 License

MIT License — free and open source ❤️
💡 Notes

    Adjust MongoDB connection in app.py if needed.

    Make sure your MongoDB data has expected fields for best results.

    Feel free to customize and extend!