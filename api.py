from config import API_KEY
from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_service import authenticate_admin, create_token, verify_token
from database_service import (
    init_db,
    get_all_users,
    get_filtered_users,
    get_total_users_count,
    get_user_by_id,
    get_user_by_name,
    create_user,
    update_user,
    delete_user
)

app = Flask(__name__)
CORS(app)
init_db()

def require_jwt():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, (jsonify({"error": "Missing Authorization header"}), 401)
    
    if not auth_header.startswith("Bearer "):
        return None, (jsonify({"error": "Invalid Authorization header format"}), 401)
    
    token = auth_header.split(" ", 1)[1]
    payload = verify_token(token)

    if not payload:
        return None, (jsonify({"error": "Invalid or expired token"}), 401)

    return payload, None

def require_role(required_role):
    def decorator_function(payload):
        if payload.get("role") != required_role:
            return jsonify({"error": "Forbidden: insufficient permissions"}), 403
        return None
    return decorator_function

@app.route("/")
def home():
    return jsonify({"message": "User Database API running"})

@app.route("/users", methods=["GET"])
def get_users():
    country = request.args.get("country")
    game = request.args.get("game")

    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "page and limit must be integers"}), 400
    
    if page < 1 or limit < 1:
        return jsonify({"error": "page and limit must be greater than 0"}), 400
    
    users = get_filtered_users(country=country, game=game, page=page, limit=limit)
    total = get_total_users_count(country=country, game=game)

    total_pages = (total + limit - 1) // limit # cieling division

    return jsonify({
        "page": page,
        "limit": limit,
        "count": len(users),
        "total": total,
        "total_pages": total_pages,
        "users": users
    })

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Request body must be json"}), 400
    
    admin = authenticate_admin(username, password)

    if not admin:
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = create_token(admin)

    return jsonify({
        "message": "Login successful",
        "token": token
    })

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route("/users", methods=["POST"])
def create_user_api():
    payload, auth_error = require_jwt()
    if auth_error:
        return auth_error
    
    role_error = require_role("admin")(payload)
    if role_error:
        return role_error
    
    data = request.json

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ["name", "age", "color", "game", "country"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if not isinstance(data["age"], int) or data["age"] < 0:
        return jsonify({"error": "Age must be a positive integer"}), 400

    if get_user_by_name(data["name"].strip().lower()):
        return jsonify({"error": "User with that name already exists"}), 409

    user_id = create_user(
        data["name"].strip().lower(),
        data["age"],
        data["color"].strip().lower(),
        data["game"].strip().lower(),
        data["country"].strip().lower()
    )

    new_user = get_user_by_id(user_id)
    return jsonify({"message": "User created", "user": new_user}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user_api(user_id):
    payload, auth_error = require_jwt()
    if auth_error:
        return auth_error
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error:": "User not found"}), 404
    
    #RBAC + ownwership check
    if payload["role"] != "admin" and payload["username"] != user["name"]:
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.json

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if "age" in data:
        if not isinstance(data["age"], int) or data["age"] < 0:
            return jsonify({"error": "Age must be a positive integer"}), 400

    if "name" in data:
        existing = get_user_by_name(data["name"].strip().lower())
        if existing and existing["id"] != user_id:
            return jsonify({"error": "User with that name already exists"}), 409

    update_user(
        user_id,
        name=data["name"].strip().lower() if "name" in data else None,
        age=data["age"] if "age" in data else None,
        color=data["color"].strip().lower() if "color" in data else None,
        game=data["game"].strip().lower() if "game" in data else None,
        country=data["country"].strip().lower() if "country" in data else None
    )

    updated_user = get_user_by_id(user_id)
    return jsonify({"message": "User updated", "user": updated_user})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user_api(user_id):
    payload, auth_error = require_jwt()
    if auth_error:
        return auth_error
    
    role_error = require_role("admin")(payload)
    if role_error:
        return role_error

    deleted = delete_user(user_id)
    if not deleted:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    print("Starting Flask API...")
    app.run(host="127.0.0.1", port=5000, debug=True)