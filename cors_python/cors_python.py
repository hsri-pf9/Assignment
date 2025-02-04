from flask import Flask, jsonify, request

app = Flask(__name__)

# Root endpoint
@app.route('/')
def home():
    return "Welcome to the CORS-enabled server!"

# Enable CORS for GET requests only
@app.after_request
def apply_cors(response):
    if request.method == "GET":
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"  # Allow all origins
        response.headers["Access-Control-Allow-Methods"] = "GET"  # Allow GET only
    return response

# Example API endpoint
@app.route('/api/get-data', methods=['GET'])
def get_data():
    return jsonify({"message": "CORS is enabled for GET requests only!"})

if __name__ == "__main__":
    app.run(port=5000)
