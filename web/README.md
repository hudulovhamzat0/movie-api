# IMDb Search Flask Application

A Flask web application that provides real-time search functionality for IMDb data stored in MongoDB. The application supports searching movies, actors, and other IMDb entities with live suggestions and comprehensive search capabilities.

## Features

- **Real-time Search**: Live search functionality with instant results
- **Auto-completion**: Smart suggestions as you type
- **Multiple Data Types**: Support for movies, actors, and other IMDb entities
- **Flexible Schema**: Automatically detects available fields in your MongoDB collection
- **REST API**: Clean API endpoints for integration
- **Database Statistics**: View collection information and stats

## Prerequisites

- Python 3.7+
- MongoDB 4.0+
- Flask
- PyMongo

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hudulovhamzat0/movie-api.git
   cd imdb-flask-app
   ```

2. **Create project structure**
   ```bash
   mkdir -p templates static/css static/js
   ```

3. **Install dependencies**
   ```bash
   pip install flask pymongo
   ```

4. **Create the frontend files**
   
   **templates/index.html** (Main HTML template):
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8" />
       <meta name="viewport" content="width=device-width, initial-scale=1" />
       <title>IMDb Search - Google Style</title>
       <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}" />
   </head>
   <body>
       <div class="container" id="container">
           <h1 class="logo" id="logo">IMDb Search</h1>
           <div class="search-container">
               <input type="text" class="search-box" id="searchBox" 
                      placeholder="Search movies, series, actors..." autocomplete="off" />
               <div class="search-icon">🔍</div>
               <div class="suggestions" id="suggestions"></div>
           </div>
           <div class="loading" id="loading">
               <div class="spinner"></div>
               <div>Searching...</div>
           </div>
           <div class="results-container" id="resultsContainer">
               <div class="results-header" id="resultsHeader"></div>
               <div id="results"></div>
           </div>
           <div class="no-results" id="noResults">
               <h3>🎬 No results found</h3>
               <p>Try different keywords</p>
           </div>
       </div>
       <div class="stats" id="stats">Loading...</div>
       <script src="{{ url_for('static', filename='js/main.js') }}"></script>
   </body>
   </html>
   ```

   **static/css/index.css** (Complete styling provided in your files)

   **static/js/main.js** (Frontend JavaScript for search functionality)

5. **Set up MongoDB**
   - Ensure MongoDB is running on `localhost:27017`
   - Create a database named `imdb_database`
   - Import your IMDb data into a collection named `movies`

6. **Prepare your data**
   Your MongoDB collection should contain IMDb data with fields such as:
   - `primaryTitle` / `originalTitle` (for movies/shows)
   - `primaryName` (for actors/directors)
   - `genres` (movie genres)
   - `primaryProfession` (for people in the industry)

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Web interface: `http://localhost:5000`
   - API endpoints: `http://localhost:5000/api/*`

## API Endpoints

### Search
```
GET /api/search?q=<query>
```
Performs a comprehensive search across all available fields.

**Parameters:**
- `q`: Search query (minimum 2 characters)

**Response:**
```json
{
  "results": [...],
  "total": 150,
  "query": "batman"
}
```

### Suggestions
```
GET /api/suggestions?q=<query>
```
Returns auto-completion suggestions.

**Parameters:**
- `q`: Partial query string

**Response:**
```json
{
  "suggestions": ["Batman", "Batman Begins", "Batman Returns"]
}
```

### Statistics
```
GET /api/stats
```
Returns database statistics and information.

**Response:**
```json
{
  "total_documents": 10000,
  "collection_name": "movies",
  "database_name": "imdb_database",
  "sample_fields": ["primaryTitle", "genres", "startYear"]
}
```

## Configuration

### Database Settings
Modify the MongoDB connection in `app.py`:

```python
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
collection = db['your_collection_name']
```

### Server Settings
Change the host and port in the main block:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Data Schema Support

The application automatically detects and searches across these fields if present:

### Movies/Shows
- `primaryTitle`: Primary title of the movie/show
- `originalTitle`: Original title in original language
- `genres`: Movie genres (comma-separated)

### People (Actors/Directors)
- `primaryName`: Person's name
- `primaryProfession`: Professional roles

## Error Handling

The application includes comprehensive error handling:
- MongoDB connection errors
- Invalid search queries
- Missing or malformed data
- API request errors

## Development

## File Structure and Setup

The complete application requires these files:

```
imdb-flask-app/
│
├── app.py                 # Flask backend application
│
├── templates/             # Jinja2 HTML templates
│   └── index.html        # Main search interface
│
├── static/               # Static assets
│   ├── css/
│   │   └── index.css     # Main stylesheet (dark theme)
│   └── js/
│       └── main.js       # Client-side JavaScript
│
└── README.md             # Documentation
```

### Required Files Content

**Note**: You'll need to create the JavaScript file `static/js/main.js` to handle:
- Real-time search functionality
- Autocomplete suggestions
- Result rendering
- API communication
- UI state management

The JavaScript should implement:
```javascript
// Key functionality needed in main.js:
// - Search input event listeners
// - API calls to /api/search and /api/suggestions
// - Dynamic result rendering
// - Loading state management
// - Mobile responsive interactions
```

### Frontend Features

The application includes a modern, responsive web interface with:

#### Design
- **Dark Theme**: Modern dark UI with red accent colors inspired by IMDb
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Google-style Interface**: Clean, minimalist search-focused design
- **Smooth Animations**: Fade-in effects and hover transitions

#### User Experience
- **Live Search**: Real-time results as you type
- **Auto-suggestions**: Dropdown with search suggestions
- **Loading States**: Visual feedback during search operations
- **Result Cards**: Clean, card-based result display with hover effects
- **Mobile Optimized**: Touch-friendly interface for mobile users

#### HTML Template (index.html)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>IMDb Search - Google Style</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}" />
</head>
<body>
    <!-- Search interface with live suggestions -->
    <div class="container" id="container">
        <h1 class="logo" id="logo">IMDb Search</h1>
        
        <!-- Search box with autocomplete -->
        <div class="search-container">
            <input type="text" class="search-box" id="searchBox" 
                   placeholder="Search movies, series, actors..." autocomplete="off" />
            <div class="search-icon">🔍</div>
            <div class="suggestions" id="suggestions"></div>
        </div>
        
        <!-- Loading indicator -->
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div>Searching...</div>
        </div>
        
        <!-- Results display -->
        <div class="results-container" id="resultsContainer">
            <div class="results-header" id="resultsHeader"></div>
            <div id="results"></div>
        </div>
        
        <!-- No results message -->
        <div class="no-results" id="noResults">
            <h3>🎬 No results found</h3>
            <p>Try different keywords</p>
        </div>
    </div>
    
    <!-- Database statistics -->
    <div class="stats" id="stats">Loading...</div>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

#### CSS Styling Features
- **Modern Color Scheme**: Dark background with red accents (#e53935)
- **Gradient Background**: Subtle gradient from dark gray to dark red
- **Card-based Results**: Elevated result cards with shadows and hover effects
- **Responsive Typography**: Scalable fonts for different screen sizes
- **Smooth Transitions**: CSS transitions for interactive elements
- **Loading Animations**: Spinning loader with fade effects

### Adding New Search Fields

To add support for new fields, modify the search conditions in the `/api/search` route:

```python
search_conditions.append(
    {"your_new_field": {"$regex": query, "$options": "i"}}
)
```

## Performance Considerations

- **Indexing**: Create MongoDB indexes on searchable fields:
  ```javascript
  db.movies.createIndex({"primaryTitle": "text", "originalTitle": "text"})
  db.movies.createIndex({"primaryName": "text"})
  ```

- **Limiting Results**: Search results are limited to 10 items for performance
- **Caching**: Consider implementing caching for frequently searched terms

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB service is running
- Check connection string and credentials
- Verify database and collection names

### Search Not Working
- Check if your collection has the expected field names
- Verify data format in MongoDB
- Check console for error messages

### No Results Found
- Ensure your MongoDB collection contains data
- Check field names match the expected schema
- Try searching with different terms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions:
- Check the troubleshooting section
- Review MongoDB and Flask documentation
- Create an issue in the repository

---

**Note**: This application is designed to work with IMDb datasets. Ensure you have the proper rights and permissions to use IMDb data in your application.