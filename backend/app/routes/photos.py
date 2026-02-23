from flask import Blueprint, request, jsonify
from app.models.schemas import Photo, Person
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import uuid
from werkzeug.utils import secure_filename
from deepface import DeepFace
import numpy as np

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def init_photo_routes(mongo):
    photo_bp = Blueprint('photos', __name__)

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @photo_bp.route('/upload', methods=['POST'])
    @jwt_required()
    def upload_photo():
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            # --- AI PROCESSING BLOCK ---
            # 1. Extract Embeddings using DeepFace
            try:
                # We use Facenet512 for high accuracy embeddings as requested in PRD
                embedding_objs = DeepFace.represent(img_path=file_path, model_name="Facenet512", enforce_detection=False)
                
                detected_faces = []
                for emb in embedding_objs:
                    # In a real app we'd trigger a Celery task here to cluster logic.
                    # For now, we synchronously save the embedding data to Mongo.
                    detected_faces.append({
                        "box": emb.get("facial_area"),
                        "embedding": emb.get("embedding"),
                        "confidence": emb.get("face_confidence", 0)
                    })
                    
                # Store in db
                new_photo = Photo.create(
                    user_id=current_user_id,
                    file_path=file_path,
                    embeddings=[f["embedding"] for f in detected_faces],
                    detected_faces=detected_faces
                )
                new_photo['processed'] = True
                
                result = mongo.db.photos.insert_one(new_photo)
                
                # Simple Mock Clustering logic:
                # If we detect a face, we create a person record if none exists for this user just as a placeholder proof of concept.
                if detected_faces:
                    existing_person = mongo.db.persons.find_one({"user_id": current_user_id})
                    if not existing_person:
                         person_data = Person.create(user_id=current_user_id, name="Unknown Person", face_cluster_id=f"cluster_{uuid.uuid4()}", representative_image_url=file_path)
                         mongo.db.persons.insert_one(person_data)

                return jsonify({
                    "message": "Photo uploaded and processed successfully",
                    "photo_id": str(result.inserted_id),
                    "faces_detected": len(detected_faces)
                }), 201
                
            except Exception as e:
                # If AI processing fails, still save the photo but mark as unprocessed
                new_photo = Photo.create(user_id=current_user_id, file_path=file_path)
                mongo.db.photos.insert_one(new_photo)
                return jsonify({"error": f"AI processing failed: {str(e)}", "message": "Photo saved but unprocessed"}), 201
                
        return jsonify({"error": "File type not allowed"}), 400

    @photo_bp.route('/', methods=['GET'])
    @jwt_required()
    def get_photos():
        current_user_id = get_jwt_identity()
        from bson import ObjectId
        photos = list(mongo.db.photos.find({"user_id": ObjectId(current_user_id)}))
        
        # Format response
        for photo in photos:
            photo['_id'] = str(photo['_id'])
            photo['user_id'] = str(photo['user_id'])
            # Don't send massive embedding arrays to frontend
            photo.pop('embeddings', None)
            
        return jsonify(photos), 200

    return photo_bp
