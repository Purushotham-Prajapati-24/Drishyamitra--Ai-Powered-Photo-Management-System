import os
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/drishyamitra")
mongo = PyMongo(app)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret_key")
jwt = JWTManager(app)

# Register Blueprints
from app.routes.auth import init_auth_routes
from app.routes.photos import init_photo_routes
from app.routes.search import init_search_routes

app.register_blueprint(init_auth_routes(mongo), url_prefix='/api/auth')
app.register_blueprint(init_photo_routes(mongo), url_prefix='/api/photos')
app.register_blueprint(init_search_routes(mongo), url_prefix='/api/search')

@app.route('/', methods=['GET'])
def health_check():
    # Simple check to see if DB is connected
    try:
        mongo.db.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        
    return jsonify({
        "status": "online",
        "database": db_status,
        "service": "Drishyamitra API"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
