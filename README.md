# Assignments

This repository contains 3 folders for 3 different assignments:
1. CORS (Cross Origin Resource Sharing)
2. API_Throughput_Middleware
3. Monitoring using Prometheus and Grafana
---
## Cross Origin Resource Sharing (CORS)
### Overview
It is a browser mechanism which enables controlled access to resources located outside of a given domain.The protocol uses a suite of HTTP headers that define trusted web origins and associated properties such as whether authenticated access is permitted. CORS also relies on a mechanism by which browsers make a "preflight" request to the server hosting the cross-origin resource, in order to check that the server will permit the actual request. In that preflight, the browser sends headers that indicate the HTTP method and headers that will be used in the actual request.

In the folder ```cors-python``` there are 4 files each having different functionalities:
### 1. ```cors_python.py```
* This Flask server has CORS enabled only for GET requests from http://localhost:3000. It includes:
  - A **root (/)** endpoint returning a welcome message.
  - A **/api/get-data** endpoint that responds with a JSON message.
  - A middleware **(@app.after_request)** that adds CORS headers to allow GET requests from http://localhost:3000.<br/>
  
To run the server first go to the directory:- ```cd cors-python``` then run the server ```python server.py```. <br/>
The server will be accessible at http://localhost:5000. <br/>

#### CORS in This Flask Server  

This Flask server has **CORS (Cross-Origin Resource Sharing)** enabled only for **GET** requests from `http://localhost:3000`. This is handled using an `after_request` hook.  

#### **What Does `apply_cors` Do?**  
The `apply_cors` function runs **after every request** and modifies the response **before** sending it back:  

- It checks if the request method is **GET**.  
- If true, it adds the following CORS headers:  
  - `Access-Control-Allow-Origin: http://localhost:3000` → Allows requests only from this origin.  
  - `Access-Control-Allow-Methods: GET` → Restricts access to **GET** requests only.  

#### **How CORS Works Here:**  
CORS is a browser security feature that restricts web pages from making requests to a different domain or port than the one serving them.  

- A frontend running on `http://localhost:3000` can make **GET** requests to `http://localhost:5000`.  
- If a request comes from another origin (e.g., `http://google.com`), the browser **blocks** it because it's not allowed.  
- Since only **GET** is permitted, any other request method like `POST` or `PUT` will also be blocked.  

This ensures controlled access while preventing unauthorized cross-origin requests. 

### 2. ```multiple_origin_cors.py```
* This Flask server enables **CORS (Cross-Origin Resource Sharing)** for **GET** requests from two specific origins: `http://localhost:3000` and `http://localhost:4000`.
* It checks the **Origin** header and applies CORS headers only if the request comes from an allowed origin and is a **GET** request.

#### Differences from Previous Code:
- **Multiple Origins**: Supports two allowed origins (`http://localhost:3000` and `http://localhost:4000`).
- **Dynamic Origin Check**: CORS headers are applied based on the incoming request's `Origin` header.
- **Extra Header**: Adds `Access-Control-Allow-Headers` for allowing the `Content-Type` header in requests.
- **More Flexibility**: Gives more control over which origins can access the server.

#### How It Works:  
- The `apply_cors` function runs after each request and checks the **Origin** header of the incoming request.  
- If the request's origin matches one of the allowed origins (`http://localhost:3000` or `http://localhost:4000`) and the request method is **GET**, it adds the following CORS headers to the response:  
  - `Access-Control-Allow-Origin`: Set to the request's origin.  
  - `Access-Control-Allow-Methods`: Allows only **GET** requests.  
  - `Access-Control-Allow-Headers`: Permits the `Content-Type` header in requests.  

This ensures that only specific origins can make GET requests and access the API, while others are blocked.

### 3. ```preflight_cors.py```
* This Flask server enables **CORS (Cross-Origin Resource Sharing)** for **GET** requests from `http://localhost:3003` and `http://localhost:4004`.
* It also explicitly handles **preflight (OPTIONS) requests** to allow cross-origin access.

- **OPTIONS (Preflight Request):** Responds with allowed methods and headers.  
- **GET Request:** Returns a JSON message if the origin is allowed.  
- **403 Forbidden:** Blocks requests from unallowed origins.  

#### Differences from Previous Codes  

| Feature                 | **cors_python.py** | **multiple_origin_cors.py** | **preflight_cors.py** |
|-------------------------|---------------|----------------|---------------|
| **Allowed Origins**     | One (`localhost:3000`) | Two (`localhost:3000`, `4000`) | Two (`localhost:3003`, `4004`) |
| **CORS Handling**       | Global `after_request` | Checked in function | Checked in function |
| **Allowed Methods**     | `GET` only | `GET` only | `GET, OPTIONS` |
| **Preflight Handling**  | ❌ No | ❌ No | ✅ Yes |
| **403 Forbidden Response** | ❌ No | ❌ No | ✅ Yes |

#### Key Enhancements  
- **Handles Preflight Requests** (`OPTIONS`) to prevent browser CORS issues.  
- **Explicitly checks requests** instead of applying CORS globally.  
- **Blocks unallowed origins** with a `403 Forbidden` response.  

#### How This Code Works  

1. **Server Setup & Port Binding:**  
   - The Flask server runs on **port 8080** (`host='0.0.0.0', port=8080`).  
   - It listens for requests on the `/api/get-data` endpoint.  

2. **CORS Origin Validation:**  
   - The server retrieves the `Origin` header from incoming requests.  
   - If the origin is **not** in the allowed list (`http://localhost:3003`, `http://localhost:4004`), it returns `403 Forbidden`.  

3. **Preflight (`OPTIONS`) Handling:**  
   - Browsers send an `OPTIONS` request before making non-GET requests or using custom headers.  
   - If the origin is allowed, the server responds with:  
     - `Access-Control-Allow-Origin`: Set dynamically to the request’s origin.  
     - `Access-Control-Allow-Methods`: Allows **GET, OPTIONS**.  
     - `Access-Control-Allow-Headers`: Allows **Content-Type** header.  
   - This response ensures the browser allows the actual request.  

4. **GET Request Handling:**  
   - If the request method is **GET** and the origin is allowed:  
     - The server responds with JSON data: `{"message": "CORS is enabled for GET requests only!"}`.  
     - `Access-Control-Allow-Origin` is dynamically set for the response.  

5. **Security & Restrictions:**  
   - **Unauthorized origins** receive `403 Forbidden`.  
   - **Only GET and OPTIONS** are permitted; other methods are blocked.  

#### **Port Mapping & Behavior**  
- **Frontend (`http://localhost:3003` or `http://localhost:4004`)** sends requests.  
- **Backend (`http://localhost:8080`)** processes and validates them.  
- **Preflight (`OPTIONS`) requests** are handled explicitly to prevent browser CORS errors.

### 4. ```test.html```
* There are two HTML codes in the test.html  

#### **1st HTML code (Basic CORS Test)**  
- Sends a **simple GET request** to `http://localhost:5000/api/get-data`.  
- If CORS is enabled on the backend, the response is logged in the browser console.  
- If CORS is **not** allowed, the browser blocks the request, logging a CORS error.  

#### **2nd HTML code (CORS with Preflight Request)**  
- Sends a **GET request with a `Content-Type` header** to `http://localhost:8080/api/get-data`.  
- The extra header **triggers a preflight (`OPTIONS`) request** before the actual GET request.  
- The browser first sends an `OPTIONS` request to check allowed methods and headers.  
- If the backend handles preflight correctly, the actual request proceeds; otherwise, CORS fails.  

#### **How to Run the HTML Files**  
1. Save the file as `test.html`.  
2. Open a terminal and start a simple HTTP server:  

   ```sh
   python3 -m http.server 3000  # Runs on http://localhost:3000
---

## API Throughput Middleware
### Overview
In this assignment which is in the folder ```API_Throughput_Middleware``` I ran two python servers one is ```ping_pong_with_flask.py``` and second one is ```ping_pong_without_flask.py``` using Python’s built-in `http.server`, The aim was to see what is the difference if we create a server with flask and without flask. This project is designed to compare the performance of two different server implementations handling the same API endpoints. The servers expose `/ping` and `/invalid` endpoints, and a middleware component tracks API throughput, latency, and success/failure rates.

### Objective
The objective of this project is to:
- Compare a Flask-based server (`ping_pong_with_flask.py`) and a standard HTTP server (`ping_pong_without_flask.py`).
- Measure API throughput using middleware to track request success, failure rates, and latency.
- Automatically send requests to both servers and analyze performance.

## How It Works
1. **Two servers are started**:
   - A Flask-based server running on port `3002`.
   - A basic HTTP server running on port `3001`.
2. **Requests are automatically sent** to both servers (`25` requests each).
3. **Middleware logs and measures request performance**, including success/failure rates and request latency.
4. **Results are printed** after all requests are processed.

### Explanation

#### 1. `main.py` (Entry Point)
This file is responsible for:
- Launching both the Flask server and the HTTP server in separate threads.
- Sending 25 requests to each server.
- Printing the responses and performance metrics.

#### 2. `ping_pong_with_flask.py` (Flask-Based Server)
This file defines a Flask server with two endpoints:
- `/ping` → Responds with `{ "message": "pong" }`.
- `/invalid` → Responds with `{ "error": "Not Found" }` (404 error).
- It uses the `Middleware` class to track request performance.

#### 3. `ping_pong_without_flask.py` (HTTP Server Without Flask)
This file creates a simple HTTP server using Python’s `http.server`. It defines:
- `/ping` → Responds with `{ "message": "pong" }`.
- Any other route returns `{ "error": "Invalid endpoint" }` (404 error).
- It also uses the `Middleware` class to track request performance.

### 4. `middleware.py` (Performance Tracker)
This module is responsible for:
- Tracking total API requests, successful requests, and failed requests.
- Calculating success rate, failure rate, and request latency.
- Logging performance metrics to the console.

### Running the Project

1. **Install dependencies** (if using Flask):
   ```sh
   pip install flask requests
   ```
2. **Run the script:**
   ```sh
   python main.py
   ```
3. **Expected Output:**
   - Each request’s response from both servers.
   - Metrics, including total requests, success rates, and request latency.
---

## Prometheus and Grafana monitoring
### Overview
I have a folder named ```Prometheus```. This implementation extends the Flask server by integrating Prometheus to track and expose HTTP request metrics.

### **How It Works**
- A **Prometheus Counter** (`total_http_requests`) tracks the number of HTTP requests received.
- The `/ping` endpoint increments the counter and responds with `"pong"`.
- The `/metrics` endpoint exposes Prometheus metrics, which can be scraped by Prometheus for monitoring.
- The Flask application uses `DispatcherMiddleware` to serve the metrics.

### **Code Explanation**
1. **`http_request_counter`**: A Prometheus Counter that increments every time the `/ping` endpoint is accessed.
2. **`/ping` Route**: Responds with `"pong"` and increments the counter.
3. **`/metrics` Endpoint**: Serves Prometheus metrics, allowing Prometheus to scrape data.
4. **Flask Application Runs on Port 8000**.
5. **Dockerized Deployment** using a `Dockerfile`.

### **Running the Flask Server in Docker**
#### **1. Created a `requirements.txt` file**
Ensure that your `requirements.txt` file contains the necessary dependencies:

```
flask
prometheus_client
werkzeug
```

#### **2. Build and Run the Docker Container**
#### **Step 1: Build the Docker Image**
```sh
docker build -t flask-prometheus-app .
```

#### **Step 2: Run the Container**
```sh
docker run -d --name flask_app -p 8000:8000 flask-prometheus-app
```

#### **3. Access the Flask Server**
- `http://localhost:8000/ping` → Responds with `pong`
- `http://localhost:8000/metrics` → Exposes Prometheus metrics

### **Setting Up Prometheus and Grafana in Docker**

#### **1. Run Prometheus in Docker**
Pull and run Prometheus:

```sh
docker run -d --name=prometheus -p 9090:9090 prom/prometheus
```

#### **2. Configure Prometheus**
Create a Prometheus config file (`prometheus.yml`):

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'flask_app'
    static_configs:
      - targets: ['host.docker.internal:8000']
```

Run Prometheus with the config:

```sh
docker run -d --name=prometheus -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

Check Prometheus UI at:  
**[http://localhost:9090](http://localhost:9090)**  

Query `total_http_requests` to see request counts.

#### **3. Run Grafana in Docker**
Pull and run Grafana:

```sh
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

Access Grafana at:  
**[http://localhost:3000](http://localhost:3000)**  
(Default login: **admin / admin**)

### **4. Add Prometheus as a Data Source in Grafana**
1. Open Grafana (`http://localhost:3000`).
2. Navigate to **Configuration > Data Sources**.
3. Click **"Add data source"** and select **Prometheus**.
4. Set URL to: `http://host.docker.internal:9090`
5. Click **"Save & Test"**.

### **5. Create a Grafana Dashboard**
1. Go to **Create > Dashboard**.
2. Click **"Add a new panel"**.
3. Select **`total_http_requests`** as the metric.
4. Click **"Apply"**.

I also have two other files namend `flask-prometheus-app` and `flask-prometheus-grafana` in which I have tried doing different variations of the task. In `flask-prometheus-grafana` I tried to put the server, prometheus and grafana in the same container and then monitor the server.
