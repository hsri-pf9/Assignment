# from flask import Flask, jsonify, request

# app = Flask(__name__)

# # Define allowed origins
# ALLOWED_ORIGINS = {"http://localhost:3002", "http://localhost:4002"}

# @app.after_request
# def apply_cors(response):
#     origin = request.headers.get("Origin")
#     # Check if the origin is allowed
#     if origin in ALLOWED_ORIGINS and request.method in ["GET", "OPTIONS"]:
#         response.headers["Access-Control-Allow-Origin"] = origin
#         response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
#         response.headers["Access-Control-Allow-Headers"] = "Content-Type"
#     return response

# # Handle OPTIONS preflight request
# @app.route('/api/get-data', methods=['OPTIONS', 'GET'])
# def get_data_options():
#     if request.method == "OPTIONS":
#         # Respond to the preflight request
#         response = jsonify({"message": "Preflight request handled."})
#         return response

#     # Handle GET request
#     return jsonify({"message": "CORS is enabled for GET requests only!"})

# # Root endpoint
# @app.route('/')
# def home():
#     return "Welcome to the CORS-enabled server!"

# if __name__ == "__main__":
#     app.run(port=5000)

from flask import Flask, jsonify, request

app = Flask(__name__)

# Allowed origins
ALLOWED_ORIGINS = {"http://localhost:3003", "http://localhost:4004"}

@app.route('/api/get-data', methods=['OPTIONS', 'GET'])
def handle_request():
    origin = request.headers.get('Origin')  # Get the Origin header
    print(f"Received request from Origin: {origin}, Method: {request.method}")  # Log the request details

    response = None

    # Handle the preflight (OPTIONS) request
    if request.method == "OPTIONS":
        print("Handling OPTIONS (preflight) request")
        if origin in ALLOWED_ORIGINS:  # Check if the origin is allowed
            response = jsonify({"message": "Preflight request handled."})
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            return response

    # Handle the actual GET request
    elif request.method == "GET":
        print("Handling GET request")
        if origin in ALLOWED_ORIGINS:  # Check if the origin is allowed
            response = jsonify({"message": "CORS is enabled for GET requests only!"})
            response.headers["Access-Control-Allow-Origin"] = origin
            return response

    # If the origin is not allowed, return 403
    return jsonify({"error": "CORS not allowed"}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
