# Assignments

This repository contains 3 folders for 3 different assignments:
1. CORS (Cross Origin Resource Sharing)
2. API_Throughput_Middleware
3. Monitoring using Prometheus and Grafana
---
## Cross Origin Resource Sharing (CORS)
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

