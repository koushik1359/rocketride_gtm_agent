import json
from backend.services.rocketride_pipeline import run_pipeline


async def write_blog_post(issues: list, repo_name: str) -> str:
    """
    Runs the copywriter RocketRide pipeline with the GitHub issue feed.
    Returns a Markdown blog post.
    """
    prompt = f"""Repository: {repo_name}

GitHub issues from the last 7 days:
{json.dumps(issues, indent=2)}"""

    return await run_pipeline("copywriter", prompt)
