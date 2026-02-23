from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from groq import Groq
import json
from bson import ObjectId

def init_search_routes(mongo):
    search_bp = Blueprint('search', __name__)
    
    # Initialize Groq client
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key) if groq_api_key else None

    @search_bp.route('/intelligent', methods=['POST'])
    @jwt_required()
    def intelligent_search():
        if not client:
            return jsonify({"error": "Groq API key not configured"}), 500
            
        current_user_id = get_jwt_identity()
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400

        # Step 1: Use Groq to parse the intent of the natural language query
        # We ask Groq to output a JSON structure that we can use to query our database
        prompt = f"""
        You are an AI assistant for a photo management app called Drishyamitra.
        The user wants to find photos. Parse their natural language query into a structured JSON search format.
        
        User Query: "{query}"
        
        Output MUST be valid JSON only, like this:
        {{
            "intent": "search",
            "search_terms": {{"person_name": "name if mentioned, else null", "event": "event if mentioned, else null", "timeframe": "timeframe if mentioned, else null"}}
        }}
        """
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192", # Fast and capable enough for intent parsing
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            ai_response = chat_completion.choices[0].message.content
            search_intent = json.loads(ai_response)
            
            # Step 2: Map the parsed intent to MongoDB queries
            # For this Hackathon MVP, we look up the person by name in the Persons collection
            person_name = search_intent.get("search_terms", {}).get("person_name")
            
            results = []
            if person_name:
                # Find the person cluster associated with this user
                person = mongo.db.persons.find_one({
                    "user_id": ObjectId(current_user_id),
                    "name": {"$regex": person_name, "$options": "i"} # Case insensitive match
                })
                
                if person:
                    # In a fully fleshed out clustering system, we'd query photos containing this person's cluster ID.
                    # Since our MVP upload assigns all detected faces to one mock cluster for the user, we just return the user's photos as a PoC.
                    photos = list(mongo.db.photos.find({"user_id": ObjectId(current_user_id)}))
                    for photo in photos:
                        photo['_id'] = str(photo['_id'])
                        photo['user_id'] = str(photo['user_id'])
                        photo.pop('embeddings', None)
                        results.append(photo)
                    return jsonify({
                        "message": f"Found photos for {person_name}",
                        "parsed_intent": search_intent,
                        "data": results
                    }), 200
                else:
                    return jsonify({
                         "message": f"No person found matching {person_name} in your clusters",
                         "parsed_intent": search_intent,
                         "data": []
                    }), 200
            
            # Fallback if no specific person found
            return jsonify({
                 "message": "Query parsed, but no specific person name extracted",
                 "parsed_intent": search_intent,
                 "data": []
            }), 200

        except Exception as e:
            return jsonify({"error": f"AI Parsing failed: {str(e)}"}), 500

    return search_bp
