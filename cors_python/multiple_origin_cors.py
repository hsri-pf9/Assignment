from flask import Flask, jsonify, request

app = Flask(__name__)

# Define allowed origins
ALLOWED_ORIGINS = {"http://localhost:3000", "http://localhost:4000"}

@app.after_request
def apply_cors(response):
    # Get the Origin header from the request
    origin = request.headers.get("Origin")
    
    # Check if the origin is allowed and the method is GET
    if origin in ALLOWED_ORIGINS and request.method == "GET":
        # Add CORS headers to the response
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    
    return response

# Root endpoint
@app.route('/')
def home():
    return "Welcome to the CORS-enabled server!"

# Example API endpoint
@app.route('/api/get-data', methods=['GET'])
def get_data():
    return jsonify({"message": "CORS is enabled for GET requests only from specific origins!"})

if __name__ == "__main__":
    app.run(port=5000)
