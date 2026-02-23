from flask import Blueprint, request, jsonify
from app.models.schemas import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from pymongo.errors import DuplicateKeyError

def init_auth_routes(mongo):
    auth_bp = Blueprint('auth', __name__)

    @auth_bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({"error": "Missing required fields: name, email, password"}), 400

        # Check if user exists
        if mongo.db.users.find_one({"email": data['email']}):
             return jsonify({"error": "Email already exists"}), 409

        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), salt)

        # Create user
        new_user = User.create(
            name=data['name'],
            email=data['email'],
            password_hash=hashed_password
        )

        try:
            result = mongo.db.users.insert_one(new_user)
            return jsonify({"message": "User created successfully", "user_id": str(result.inserted_id)}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields: email, password"}), 400

        user = mongo.db.users.find_one({"email": data['email']})
        if not user:
             return jsonify({"error": "Invalid email or password"}), 401

        # Check password
        if bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash']):
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify({
                "message": "Login successful",
                "token": access_token,
                "user": {"name": user['name'], "email": user['email'], "id": str(user['_id'])}
            }), 200
        else:
             return jsonify({"error": "Invalid email or password"}), 401
             
    @auth_bp.route('/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        current_user_id = get_jwt_identity()
        from bson import ObjectId
        user = mongo.db.users.find_one({"_id": ObjectId(current_user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email']
        }), 200

    return auth_bp
