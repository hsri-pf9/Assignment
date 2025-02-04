import time
import sys

class Middleware:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = time.time()

    def log_metrics(self, success, latency):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

        success_rate = (self.successful_requests / self.total_requests) * 100
        failure_rate = (self.failed_requests / self.total_requests) * 100

        sys.stdout.write("\nMetrics:\n")
        sys.stdout.write(f"Total requests: {self.total_requests}\n")
        sys.stdout.write(f"Successful requests: {self.successful_requests} ({success_rate:.2f}%)\n")
        sys.stdout.write(f"Failed requests: {self.failed_requests} ({failure_rate:.2f}%)\n")
        sys.stdout.write(f"Request latency: {latency:.4f} seconds\n")

    def process_request(self, request, start_time):
        latency = time.time() - start_time
        
        if isinstance(request, object) and hasattr(request, "method"):
            # Handling Flask requests
            success = request.method == "GET" and request.path == "/ping"
        else:
            # Handling BaseHTTPRequestHandler (HTTP Server)
            success = getattr(request, "command", None) == "GET" and getattr(request, "path", None) == "/ping"
        
        self.log_metrics(success, latency)
