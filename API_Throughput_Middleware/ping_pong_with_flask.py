from flask import Flask, jsonify, request
import time
from middleware import Middleware

middleware = Middleware()
app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    start_time = time.time()
    response = jsonify({"message": "pong"})
    response.status_code = 200
    # Pass the request object to the middleware for logging
    middleware.process_request(request, start_time)
    return response

@app.route("/invalid", methods=["GET"])
def invalid():
    start_time = time.time()
    response = jsonify({"error": "Not Found"})
    response.status_code = 404
    # Pass the request object to the middleware for logging
    middleware.process_request(request, start_time)
    return response

def start_flask_server(port=3002):
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_flask_server()
