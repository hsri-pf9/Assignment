from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
LATENCY = Histogram('http_request_latency_seconds', 'Request latency', ['endpoint'])

@app.route('/ping')
def ping():
    REQUEST_COUNT.labels(method='GET', endpoint='/ping').inc()
    with LATENCY.labels(endpoint='/ping').time():
        return jsonify({'message': 'pong'})

@app.route('/pong')
def pong():
    REQUEST_COUNT.labels(method='GET', endpoint='/pong').inc()
    with LATENCY.labels(endpoint='/pong').time():
        return jsonify({'message': 'ping'})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
