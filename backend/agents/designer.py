from openai import OpenAI


def generate_thumbnail(client: OpenAI, blog_text: str, repo_name: str) -> str:
    """
    Reads the generated blog post, extracts a visual concept,
    and generates a promotional thumbnail using DALL-E 3.
    Returns the image URL.
    """
    # first, ask gpt to come up with a visual concept from the blog
    concept_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a graphic designer. Respond with only a single image description, nothing else."},
            {"role": "user", "content": f"""Based on this developer blog post, describe a single 
promotional thumbnail image for it. The image should be abstract and tech-themed — 
think gradients, circuits, rocket imagery, code fragments. No text in the image. 
Keep the description under 50 words.

Blog post:
{blog_text[:1500]}"""},
        ],
        temperature=0.9,
    )

    image_concept = concept_resp.choices[0].message.content

    # now hit DALL-E 3
    image_resp = client.images.generate(
        model="dall-e-3",
        prompt=f"A modern, sleek promotional thumbnail for an open-source AI project called {repo_name}. Style: {image_concept}",
        size="1792x1024",
        quality="standard",
        n=1,
    )

    return image_resp.data[0].url
