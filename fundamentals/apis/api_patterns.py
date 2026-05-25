import requests
from typing import Optional


class APIClient:
    """
    Reusable HTTP client with base URL, default headers, and error handling.
    This pattern is used in every production service that calls external APIs.
    """

    def __init__(self, base_url, api_key=None, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout  = timeout
        self.session  = requests.Session()

        # Session reuses TCP connection — faster for multiple requests
        self.session.headers.update({
            "Accept":       "application/json",
            "Content-Type": "application/json",
            "User-Agent":   "PythonLearningJourney/1.0",
        })

        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"

    def get(self, endpoint, params=None):
        """Make a GET request and return parsed JSON or None on error."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP error on GET {url}: {e}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"  Connection error: cannot reach {self.base_url}")
            return None
        except requests.exceptions.Timeout:
            print(f"  Timeout on GET {url}")
            return None

    def post(self, endpoint, data):
        """Make a POST request with JSON body."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  Request error on POST {url}: {e}")
            return None

    def close(self):
        self.session.close()


# --- Using the client ---
print("=== APIClient Pattern ===")
client = APIClient("https://httpbin.org")

result = client.get("/get", params={"source": "api_patterns"})
if result:
    print(f"  Connected to: {result.get('url')}")
    print(f"  Headers sent: User-Agent = {result['headers'].get('User-Agent')}")

client.close()
print("\napi_patterns.py completed successfully.")