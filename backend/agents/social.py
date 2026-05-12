from backend.services.rocketride_pipeline import run_pipeline


async def write_twitter_thread(blog_post: str, repo_name: str) -> str:
    """
    Runs the social RocketRide pipeline with the generated blog post.
    Returns a numbered 5-tweet thread.
    """
    prompt = f"""Repository: {repo_name}

Weekly community blog post:
{blog_post}"""

    return await run_pipeline("social", prompt)
