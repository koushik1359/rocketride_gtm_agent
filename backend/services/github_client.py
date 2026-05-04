import requests
from datetime import datetime, timedelta


GITHUB_API = "https://api.github.com"


def fetch_issues(repo, days_back=7, max_results=30):
    """
    Pull recently active issues from a GitHub repo.
    Skips pull requests — we only want community discussions and bug reports.
    """
    cutoff = (datetime.now() - timedelta(days=days_back)).isoformat()

    resp = requests.get(
        f"{GITHUB_API}/repos/{repo}/issues",
        params={"state": "all", "since": cutoff, "per_page": max_results},
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    resp.raise_for_status()

    raw = resp.json()

    # filter out PRs — github returns them mixed in with issues
    issues = [i for i in raw if "pull_request" not in i]

    return _clean(issues)


def _clean(issues):
    """Strip down to just the fields our agents care about."""
    cleaned = []
    for issue in issues:
        labels = [l["name"] for l in issue.get("labels", [])]

        cleaned.append({
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "comments": issue["comments"],
            "labels": labels,
            "url": issue["html_url"],
            "created": issue["created_at"][:10],
            "author": issue["user"]["login"],
        })

    return cleaned
