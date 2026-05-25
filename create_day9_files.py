from pathlib import Path

files = {}

files["fundamentals/apis/__init__.py"] = ""

files["fundamentals/apis/http_basics.py"] = """
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


print("\\n=== Sending Parameters ===")
# Query parameters appear in URL: ?key=value&key2=value2
params = {"page": 1, "per_page": 5}
response = requests.get("https://httpbin.org/get", params=params, timeout=10)
data = response.json()
print(f"  Full URL    : {data.get('url')}")
print(f"  Args sent   : {data.get('args')}")


print("\\n=== POST Request ===")
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


print("\\n=== Error Handling ===")
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

print("\\nhttp_basics.py completed successfully.")
""".strip()

files["fundamentals/apis/api_patterns.py"] = """
import requests
from typing import Optional


class APIClient:
    \"\"\"
    Reusable HTTP client with base URL, default headers, and error handling.
    This pattern is used in every production service that calls external APIs.
    \"\"\"

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
        \"\"\"Make a GET request and return parsed JSON or None on error.\"\"\"
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
        \"\"\"Make a POST request with JSON body.\"\"\"
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
print("\\napi_patterns.py completed successfully.")
""".strip()

files["mini_projects/github_analyzer/__init__.py"] = ""

files["mini_projects/github_analyzer/github_analyzer.py"] = """
\"\"\"
github_analyzer.py

Fetches and analyzes real data from the GitHub public API.
Demonstrates real HTTP requests, JSON processing, and error handling.

GitHub API docs: https://docs.github.com/en/rest
No API key required for public data (60 requests/hour limit).

Usage:
    python mini_projects/github_analyzer/github_analyzer.py
\"\"\"

import requests
from datetime import datetime


GITHUB_API_BASE = "https://api.github.com"
HEADERS = {
    "Accept":     "application/vnd.github.v3+json",
    "User-Agent": "PythonLearningJourney",
}


def get_user_profile(username):
    \"\"\"Fetch public profile data for a GitHub user.\"\"\"
    url = f"{GITHUB_API_BASE}/users/{username}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"  User not found: {username}")
        else:
            print(f"  HTTP error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  Request failed: {e}")
        return None


def get_user_repos(username, max_repos=10):
    \"\"\"Fetch public repositories for a GitHub user.\"\"\"
    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    params = {
        "sort":      "updated",
        "direction": "desc",
        "per_page":  max_repos,
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  Failed to fetch repos: {e}")
        return []


def get_repo_languages(username, repo_name):
    \"\"\"Fetch language breakdown for a specific repository.\"\"\"
    url = f"{GITHUB_API_BASE}/repos/{username}/{repo_name}/languages"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {}


def analyze_repos(repos):
    \"\"\"
    Analyze repository list and return summary statistics.
    Demonstrates processing a real API response with loops and dicts.
    \"\"\"
    if not repos:
        return {}

    total_stars   = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks   = sum(r.get("forks_count", 0) for r in repos)
    languages     = [r.get("language") for r in repos if r.get("language")]
    language_counts = {}
    for lang in languages:
        language_counts.setdefault(lang, 0)
        language_counts[lang] += 1

    top_repo = max(repos, key=lambda r: r.get("stargazers_count", 0))

    return {
        "total_repos":      len(repos),
        "total_stars":      total_stars,
        "total_forks":      total_forks,
        "languages":        language_counts,
        "top_repo":         top_repo.get("name"),
        "top_repo_stars":   top_repo.get("stargazers_count", 0),
    }


def generate_profile_report(username):
    \"\"\"Fetch all data and generate a full profile report.\"\"\"
    print(f"Fetching GitHub profile: {username}\\n")

    profile = get_user_profile(username)
    if not profile:
        return

    repos = get_user_repos(username, max_repos=10)
    stats = analyze_repos(repos)

    print("=" * 55)
    print(f"  GITHUB PROFILE: {profile.get('login')}")
    print("=" * 55)
    print(f"  Name        : {profile.get('name', 'Not specified')}")
    print(f"  Bio         : {profile.get('bio', 'No bio')}")
    print(f"  Location    : {profile.get('location', 'Not specified')}")
    print(f"  Company     : {profile.get('company', 'Not specified')}")
    print(f"  Followers   : {profile.get('followers', 0)}")
    print(f"  Following   : {profile.get('following', 0)}")
    print(f"  Public repos: {profile.get('public_repos', 0)}")

    joined = profile.get("created_at", "")
    if joined:
        joined_date = datetime.strptime(joined, "%Y-%m-%dT%H:%M:%SZ")
        print(f"  Joined      : {joined_date.strftime('%B %Y')}")

    if stats:
        print(f"\\n  REPOSITORY STATS (last {stats['total_repos']} repos):")
        print(f"    Total stars : {stats['total_stars']}")
        print(f"    Total forks : {stats['total_forks']}")
        print(f"    Top repo    : {stats['top_repo']} ({stats['top_repo_stars']} stars)")

        if stats["languages"]:
            print(f"\\n  LANGUAGES USED:")
            for lang, count in sorted(
                stats["languages"].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                bar = "=" * (count * 3)
                print(f"    {lang:<15} {bar} ({count} repos)")

    if repos:
        print(f"\\n  RECENT REPOSITORIES:")
        for repo in repos[:5]:
            stars    = repo.get("stargazers_count", 0)
            language = repo.get("language") or "Unknown"
            print(
                f"    {repo['name']:<35} "
                f"[{language:<12}] "
                f"★ {stars}"
            )

    print("=" * 55)


if __name__ == "__main__":
    # Analyze your own GitHub profile
    generate_profile_report("Devika-Bairagoni")

    print()

    # Also analyze a well-known profile to see richer data
    generate_profile_report("torvalds")
""".strip()

for filepath, content in files.items():
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")

print("\nAll Day 9 files created successfully.")