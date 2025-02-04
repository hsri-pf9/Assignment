from flask import Flask
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

http_request_counter = Counter('total_http_requests', 'Total number of HTTP requests received')

@app.route('/ping')
def handle_ping():
    http_request_counter.inc()
    return 'pong\n'

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/metrics': make_wsgi_app()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
