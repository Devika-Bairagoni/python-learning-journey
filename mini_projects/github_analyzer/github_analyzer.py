"""
github_analyzer.py

Fetches and analyzes real data from the GitHub public API.
Demonstrates real HTTP requests, JSON processing, and error handling.

GitHub API docs: https://docs.github.com/en/rest
No API key required for public data (60 requests/hour limit).

Usage:
    python mini_projects/github_analyzer/github_analyzer.py
"""

import requests
from datetime import datetime


GITHUB_API_BASE = "https://api.github.com"
HEADERS = {
    "Accept":     "application/vnd.github.v3+json",
    "User-Agent": "PythonLearningJourney",
}


def get_user_profile(username):
    """Fetch public profile data for a GitHub user."""
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
    """Fetch public repositories for a GitHub user."""
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
    """Fetch language breakdown for a specific repository."""
    url = f"{GITHUB_API_BASE}/repos/{username}/{repo_name}/languages"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {}


def analyze_repos(repos):
    """
    Analyze repository list and return summary statistics.
    Demonstrates processing a real API response with loops and dicts.
    """
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
    """Fetch all data and generate a full profile report."""
    print(f"Fetching GitHub profile: {username}\n")

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
        print(f"\n  REPOSITORY STATS (last {stats['total_repos']} repos):")
        print(f"    Total stars : {stats['total_stars']}")
        print(f"    Total forks : {stats['total_forks']}")
        print(f"    Top repo    : {stats['top_repo']} ({stats['top_repo_stars']} stars)")

        if stats["languages"]:
            print(f"\n  LANGUAGES USED:")
            for lang, count in sorted(
                stats["languages"].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                bar = "=" * (count * 3)
                print(f"    {lang:<15} {bar} ({count} repos)")

    if repos:
        print(f"\n  RECENT REPOSITORIES:")
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