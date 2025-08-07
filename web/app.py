from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import re
from bson import ObjectId
import json

app = Flask(__name__)

# MongoDB bağlantısı
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['imdb_database']
    collection = db['movies']  # Collection adınızı buraya yazın
    print("✅ MongoDB bağlantısı başarılı!")
except Exception as e:
    print(f"❌ MongoDB bağlantı hatası: {e}")

class JSONEncoder(json.JSONEncoder):
    """MongoDB ObjectId için JSON encoder"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/search')
def search():
    """Canlı arama API"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify({'results': [], 'total': 0})
        
        # MongoDB text search sorguları
        search_conditions = []
        
        # Title search (case insensitive)
        if 'primaryTitle' in collection.find_one() or {}:
            search_conditions.extend([
                {"primaryTitle": {"$regex": query, "$options": "i"}},
                {"originalTitle": {"$regex": query, "$options": "i"}}
            ])
        
        # Name search (name.basics için)
        if 'primaryName' in collection.find_one() or {}:
            search_conditions.append(
                {"primaryName": {"$regex": query, "$options": "i"}}
            )
        
        # Genres search
        if 'genres' in collection.find_one() or {}:
            search_conditions.append(
                {"genres": {"$regex": query, "$options": "i"}}
            )
        
        # Profession search (name.basics için)
        if 'primaryProfession' in collection.find_one() or {}:
            search_conditions.append(
                {"primaryProfession": {"$regex": query, "$options": "i"}}
            )
        
        if not search_conditions:
            return jsonify({'results': [], 'total': 0, 'error': 'No searchable fields found'})
        
        # MongoDB sorgusu
        mongo_query = {"$or": search_conditions}
        
        # Sonuçları getir (limit 10)
        results = list(collection.find(mongo_query).limit(10))
        total = collection.count_documents(mongo_query)
        
        # ObjectId'leri temizle
        for result in results:
            if '_id' in result:
                result['_id'] = str(result['_id'])
        
        return jsonify({
            'results': results,
            'total': total,
            'query': query
        })
        
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({'results': [], 'total': 0, 'error': str(e)})

@app.route('/api/suggestions')
def suggestions():
    """Otomatik tamamlama önerileri"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify({'suggestions': []})
        
        # Benzersiz öneriler için aggregation pipeline
        pipeline = []
        
        # Title suggestions
        sample_doc = collection.find_one()
        if sample_doc and 'primaryTitle' in sample_doc:
            pipeline = [
                {"$match": {"primaryTitle": {"$regex": f"^{query}", "$options": "i"}}},
                {"$group": {"_id": "$primaryTitle"}},
                {"$limit": 5},
                {"$project": {"_id": 0, "suggestion": "$_id"}}
            ]
        elif sample_doc and 'primaryName' in sample_doc:
            pipeline = [
                {"$match": {"primaryName": {"$regex": f"^{query}", "$options": "i"}}},
                {"$group": {"_id": "$primaryName"}},
                {"$limit": 5},
                {"$project": {"_id": 0, "suggestion": "$_id"}}
            ]
        
        if pipeline:
            suggestions = list(collection.aggregate(pipeline))
            return jsonify({
                'suggestions': [s['suggestion'] for s in suggestions]
            })
        
        return jsonify({'suggestions': []})
        
    except Exception as e:
        print(f"Suggestions error: {e}")
        return jsonify({'suggestions': []})

@app.route('/api/stats')
def stats():
    """Database istatistikleri"""
    try:
        total_docs = collection.count_documents({})
        sample_doc = collection.find_one()
        
        stats_data = {
            'total_documents': total_docs,
            'collection_name': collection.name,
            'database_name': db.name
        }
        
        if sample_doc:
            stats_data['sample_fields'] = list(sample_doc.keys())
            if '_id' in stats_data['sample_fields']:
                stats_data['sample_fields'].remove('_id')
        
        return jsonify(stats_data)
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)