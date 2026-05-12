import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from dotenv import load_dotenv

from backend.services.github_client import fetch_issues
from backend.agents.copywriter import write_blog_post
from backend.agents.social import write_twitter_thread
from backend.agents.producer import write_video_script
from backend.agents.designer import generate_thumbnail

load_dotenv()

app = FastAPI(title="RocketRide GTM Agent")

_raw_origins = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [o.strip() for o in _raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AsyncOpenAI client used only for DALL-E 3 thumbnail generation
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_REPO = "rocketride-org/rocketride-server"


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/run")
async def run_agents(repo: str = DEFAULT_REPO):
    """
    Main endpoint. Fetches GitHub issue data, runs 4 RocketRide pipelines
    in sequence, and returns the full GTM campaign payload.

    Pipeline execution order:
      1. copywriter.pipe  — generates the weekly community blog post
      2. social.pipe      — distils the blog into a 5-tweet thread
      3. producer.pipe    — writes a 30-second short-form video script
      4. designer.pipe    — produces a DALL-E 3 image prompt; DALL-E renders it
    """
    # Step 1: fetch GitHub activity
    issues = fetch_issues(repo)

    # Step 2: copywriter pipeline → blog post
    blog = await write_blog_post(issues, repo)

    # Step 3: social + producer pipelines take the blog as input
    thread = await write_twitter_thread(blog, repo)
    script = await write_video_script(blog, repo)

    # Step 4: designer pipeline → image concept → DALL-E 3 render
    image_url = await generate_thumbnail(openai_client, blog, repo)

    return {
        "repo": repo,
        "issues_analyzed": len(issues),
        "blog_post": blog,
        "twitter_thread": thread,
        "video_script": script,
        "thumbnail_url": image_url,
    }
