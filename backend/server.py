import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

from backend.services.github_client import fetch_issues
from backend.agents.copywriter import write_blog_post
from backend.agents.social import write_twitter_thread
from backend.agents.producer import write_video_script
from backend.agents.designer import generate_thumbnail

load_dotenv()

app = FastAPI(title="RocketRide GTM Command Center")

# Comma-separated list of allowed origins; set FRONTEND_URL in Azure App Settings
_raw_origins = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [o.strip() for o in _raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_REPO = "rocketride-org/rocketride-server"


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/run")
def run_agents(repo: str = DEFAULT_REPO):
    """
    Main endpoint. Fetches GitHub data, runs all 4 agents,
    and returns the full campaign payload.
    """
    # step 1: gather data
    issues = fetch_issues(repo)

    # step 2: run the text agents
    blog = write_blog_post(client, issues, repo)
    thread = write_twitter_thread(client, issues, repo)
    script = write_video_script(client, issues, repo)

    # step 3: generate the thumbnail from the blog content
    image_url = generate_thumbnail(client, blog, repo)

    return {
        "repo": repo,
        "issues_analyzed": len(issues),
        "blog_post": blog,
        "twitter_thread": thread,
        "video_script": script,
        "thumbnail_url": image_url,
    }
