import threading
import time
import requests
from ping_pong_without_flask import start_http_server
from ping_pong_with_flask import start_flask_server

def run_http_server():
    start_http_server(port=3001)

def run_flask_server():
    start_flask_server(port=3002)

def send_requests():
    """Send 25 requests to both Flask and HTTP servers automatically."""
    time.sleep(2)  # Give some time for servers to start
    flask_url = "http://localhost:3002/ping"
    http_url = "http://localhost:3001/ping"
    
    for i in range(25):  # Send 25 requests
        try:
            response_flask = requests.get(flask_url)
            print(f"Flask Server Response {i+1}: {response_flask.json()}")

            response_http = requests.get(http_url)
            print(f"HTTP Server Response {i+1}: {response_http.json()}")

            time.sleep(0.5)  # Small delay between requests
        except requests.exceptions.ConnectionError:
            print("Server not ready yet. Retrying...")
            time.sleep(1)

    print("\nCompleted all requests. Shutting down...")

if __name__ == "__main__":
    # Start both servers as daemon threads
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    http_thread = threading.Thread(target=run_http_server, daemon=True)

    flask_thread.start()
    http_thread.start()

    # Run the requests automatically
    send_requests()
    
    print("Servers have processed the requests. Exiting.")
