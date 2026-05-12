from backend.services.rocketride_pipeline import run_pipeline


async def write_video_script(blog_post: str, repo_name: str) -> str:
    """
    Runs the producer RocketRide pipeline with the generated blog post.
    Returns a 30-second short-form video script.
    """
    prompt = f"""Repository: {repo_name}

Weekly community blog post:
{blog_post}"""

    return await run_pipeline("producer", prompt)
