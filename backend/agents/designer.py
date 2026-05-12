from openai import AsyncOpenAI
from backend.services.rocketride_pipeline import run_pipeline


async def generate_thumbnail(openai_client: AsyncOpenAI, blog_text: str, repo_name: str) -> str:
    """
    Uses the designer RocketRide pipeline to generate a DALL-E 3 image prompt
    from the blog post, then calls DALL-E 3 directly to render the thumbnail.
    Returns the image URL.
    """
    # Step 1: RocketRide designer pipeline generates the visual concept
    image_concept = await run_pipeline("designer", blog_text[:2000])

    # Step 2: DALL-E 3 renders the concept (no image generation node in RocketRide)
    image_resp = await openai_client.images.generate(
        model="dall-e-3",
        prompt=f"Promotional thumbnail for open-source AI project {repo_name}. {image_concept}",
        size="1792x1024",
        quality="standard",
        n=1,
    )

    return image_resp.data[0].url
