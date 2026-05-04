# RocketRide GTM Agent

> **Turn a week of GitHub activity into a full marketing campaign in 30 seconds.**

Built as part of the RocketRide AI Growth Intern challenge. This tool solves a real problem for open-source teams: the gap between shipping great work and telling the world about it. Every week, RocketRide and projects like it generate dozens of issues, fixes, and community discussions that never get communicated beyond GitHub. This agent closes that gap automatically.

Point it at any GitHub repository. In under 60 seconds, four specialized AI agents analyze the last 7 days of issue activity and produce a complete, publish-ready GTM campaign: community blog post, Twitter thread, short-form video script, and a DALL-E 3 promotional thumbnail. No templates, no manual writing. Just signal in, content out.

**Live Demo: [happy-mushroom-0447b8210.7.azurestaticapps.net](https://happy-mushroom-0447b8210.7.azurestaticapps.net)**

> Try it on `rocketride-org/rocketride-server` to see it run against RocketRide's own repo.

![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Python%203.12-009688?style=flat-square&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini%20%2B%20DALL--E%203-412991?style=flat-square&logo=openai)
![Azure](https://img.shields.io/badge/Azure-Container%20Apps%20%2B%20Static%20Web%20Apps-0078D4?style=flat-square&logo=microsoftazure)

---

## The Problem This Solves

Open-source maintainers are builders, not marketers. Great work gets shipped every week (bug fixes, new features, community milestones) but most of it disappears into a closed GitHub issue. There's no time to write blog posts, craft Twitter threads, or produce video content on top of everything else.

RocketRide GTM Agent automates the entire content pipeline. It reads your GitHub activity, understands what happened, and generates everything a growth team would produce manually. In the time it takes to make a coffee.

This is the kind of tooling the AI Growth Intern role is about: using agentic AI to do real work, not demos.

---

## How It Works

Four agents fire in sequence against your GitHub repo:

| Agent | What it does | Output |
|-------|-------------|--------|
| **Researcher** | Pulls last 7 days of issues via GitHub REST API, filters PRs, cleans data | Structured issue feed |
| **Copywriter** | Reads the issue feed, writes a weekly community update in the voice of a real dev advocate | Markdown blog post |
| **Social** | Distills the blog post into a 5-tweet thread with a hook, content beats, and CTA | Twitter thread |
| **Producer** | Writes a 30-second short-form video script optimized for TikTok / Reels pacing | Video script |
| **Designer** | GPT-4o-mini describes a visual concept from the blog; DALL-E 3 renders it | Promotional thumbnail |

Everything lands in a split-screen UI: full blog post on the left, socials and media stacked on the right, ready to copy and publish.

---

## Architecture

```
User enters GitHub repo (owner/repo)
        |
        v
+------------------------------------------+
|         Next.js 16 Frontend              |
|   (Azure Static Web Apps - Free tier)    |
+------------------+-----------------------+
                   |  POST /api/run?repo=...
                   v
+------------------------------------------+
|       FastAPI Backend (Docker)           |
|   (Azure Container Apps - Free tier)     |
|                                          |
|  +----------+  +----------+             |
|  |Copywriter|  |  Social  |             |
|  +----------+  +----------+             |
|  +----------+  +----------+             |
|  | Producer |  | Designer |             |
|  +----------+  +----------+             |
+------------------+-----------------------+
                   |
                   v
         OpenAI API (GPT-4o-mini + DALL-E 3)
```

---

## Tech Stack

**Frontend**
- [Next.js 16](https://nextjs.org/) with React 19 App Router
- [Tailwind CSS v4](https://tailwindcss.com/) for utility-first styling
- [Framer Motion](https://www.framer.com/motion/) for animations
- [Lucide React](https://lucide.dev/) for icons
- [React Markdown](https://github.com/remarkjs/react-markdown) to render the generated blog post

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) async Python web framework
- [Uvicorn](https://www.uvicorn.org/) ASGI server
- [OpenAI Python SDK v2](https://github.com/openai/openai-python) for GPT-4o-mini and DALL-E 3
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management

**Infrastructure**
- Azure Container Apps for the backend (consumption-based, no VM quota limits)
- Azure Container Registry for Docker image storage
- Azure Static Web Apps for the frontend (free tier)
- GitHub Actions for CI/CD, auto-deploys on every push to `master`

---

## Project Structure

```
rocketride_gtm_agent/
├── backend/
│   ├── server.py              # FastAPI app, CORS, /api/run endpoint
│   ├── agents/
│   │   ├── copywriter.py      # Blog post generation (GPT-4o-mini)
│   │   ├── social.py          # Twitter thread generation
│   │   ├── producer.py        # Video script generation
│   │   └── designer.py        # Thumbnail generation (DALL-E 3)
│   └── services/
│       └── github_client.py   # GitHub REST API wrapper
├── frontend/
│   └── app/
│       ├── page.tsx           # Main UI: input, progress, results
│       ├── layout.tsx         # Root layout and metadata
│       └── globals.css        # Tailwind + custom prose styles
├── Dockerfile                 # Backend container definition
├── requirements.txt           # Python dependencies
└── .github/workflows/
    ├── backend-deploy.yml     # Build + push Docker image to Container Apps
    └── azure-static-web-apps-*.yml  # Auto-deploy frontend to Static Web Apps
```

---

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repo
```bash
git clone https://github.com/koushik1359/rocketride_gtm_agent.git
cd rocketride_gtm_agent
```

### 2. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env` and add your OpenAI key:
```
OPENAI_API_KEY=sk-...
```

### 3. Run the backend
```bash
pip install -r requirements.txt
uvicorn backend.server:app --reload --port 8000
```

### 4. Run the frontend
```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000), enter `rocketride-org/rocketride-server`, and click **Run Pipeline**.

---

## Environment Variables

| Variable | Where | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | Backend | Your OpenAI API key |
| `FRONTEND_URL` | Backend | Allowed CORS origin (comma-separated for multiple) |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API base URL (baked in at build time) |

---

## Deployment

Fully deployed on Azure, free tier:

| Service | Purpose | Cost |
|---------|---------|------|
| Azure Container Apps | FastAPI backend (Dockerized) | Free consumption tier |
| Azure Static Web Apps | Next.js frontend | Free |
| Azure Container Registry | Docker image storage | ~$5/mo (Basic) |

### CI/CD
Every push to `master` auto-deploys:
- Changes to `backend/` or `Dockerfile` trigger a Docker build, push to ACR, and Container App update
- Changes to `frontend/` trigger a Next.js build with env vars and deploy to Static Web Apps

---

## Why I Built This

Joe's brief was clear: the AI Growth Intern role is about using agentic AI to automate GTM workflows, covering community engagement, content generation, and making it easy for open-source teams to tell their story.

This is my answer to that brief. Not a prototype, not a mockup. A fully deployed, production-ready tool that does real work on real data. It runs against any GitHub repo, generates content a real dev advocate would be proud to publish, and ships the whole pipeline to Azure in under a minute via GitHub Actions.

The skills this demonstrates: multi-agent orchestration, LLM API integration, full-stack development, cloud deployment, and GTM automation. I'm ready to bring this to RocketRide's actual growth workflows from day one.
