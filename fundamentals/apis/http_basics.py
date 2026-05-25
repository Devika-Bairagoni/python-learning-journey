import requests

print("=== HTTP GET Request ===")

# Every HTTP request has:
# - Method: GET, POST, PUT, DELETE, PATCH
# - URL: where to send the request
# - Headers: metadata about the request
# - Body: data to send (POST/PUT only)
# - Response: status code + body back from server

# GET request to a public test API
url = "https://httpbin.org/get"
response = requests.get(url, timeout=10)

# Status codes you must know:
# 200 = OK, 201 = Created, 400 = Bad Request,
# 401 = Unauthorized, 404 = Not Found, 500 = Server Error

print(f"  Status code : {response.status_code}")
print(f"  OK          : {response.ok}")
print(f"  Content-Type: {response.headers.get('Content-Type')}")

# Parse JSON response body into Python dict
data = response.json()
print(f"  Origin IP   : {data.get('origin')}")
print(f"  URL called  : {data.get('url')}")


print("\n=== Sending Parameters ===")
# Query parameters appear in URL: ?key=value&key2=value2
params = {"page": 1, "per_page": 5}
response = requests.get("https://httpbin.org/get", params=params, timeout=10)
data = response.json()
print(f"  Full URL    : {data.get('url')}")
print(f"  Args sent   : {data.get('args')}")


print("\n=== POST Request ===")
# POST sends data in the request body
payload = {"username": "devika", "action": "login"}
response = requests.post(
    "https://httpbin.org/post",
    json=payload,    # json= automatically sets Content-Type header
    timeout=10
)
data = response.json()
print(f"  Status      : {response.status_code}")
print(f"  Data sent   : {data.get('json')}")


print("\n=== Error Handling ===")
# Always handle these in production

# 1. HTTP error status codes
response = requests.get("https://httpbin.org/status/404", timeout=10)
if response.status_code == 404:
    print(f"  404 Not Found — resource does not exist")

# 2. raise_for_status() — raises exception for 4xx and 5xx
try:
    response = requests.get("https://httpbin.org/status/500", timeout=10)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"  HTTP error: {e}")

# 3. Connection and timeout errors
try:
    response = requests.get("https://this-domain-does-not-exist.xyz", timeout=5)
except requests.exceptions.ConnectionError:
    print(f"  Connection error: could not reach server")
except requests.exceptions.Timeout:
    print(f"  Timeout: server took too long to respond")

print("\nhttp_basics.py completed successfully.")