import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Middleware to log throughput data
@app.before_request
def log_request_data():
    # Record the start time of the request
    request.start_time = time.time()

@app.after_request
def log_throughput_data(response):
    # Calculate the time taken for the request
    processing_time = time.time() - request.start_time
    
    # Log relevant throughput data
    app.logger.info(f"Method: {request.method} | Path: {request.path} | "
                    f"Status: {response.status_code} | Time taken: {processing_time:.4f} seconds")
    
    # Return the response to be sent to the client
    return response

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
