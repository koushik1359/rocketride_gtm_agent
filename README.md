# RocketRide GTM Agent

> **Paste a GitHub repo. Get a full marketing campaign in 30 seconds.**

An AI-powered Go-To-Market automation platform that analyzes your open-source project's latest GitHub activity and instantly generates a community blog post, Twitter thread, short-form video script, and a DALL-E 3 promotional thumbnail — all from a single click.

**Live Demo → [happy-mushroom-0447b8210.7.azurestaticapps.net](https://happy-mushroom-0447b8210.7.azurestaticapps.net)**

![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Python%203.12-009688?style=flat-square&logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini%20%2B%20DALL--E%203-412991?style=flat-square&logo=openai)
![Azure](https://img.shields.io/badge/Azure-Container%20Apps%20%2B%20Static%20Web%20Apps-0078D4?style=flat-square&logo=microsoftazure)

---

## What it does

RocketRide GTM Agent deploys a swarm of four specialized AI agents against any GitHub repository. It fetches the last 7 days of issue activity and runs four agents in sequence to produce a complete, publish-ready marketing campaign:

| Agent | Output | Model |
|-------|--------|-------|
| **Researcher** | Fetches and cleans GitHub issues | GitHub REST API |
| **Copywriter** | Weekly community blog post in Markdown | GPT-4o-mini |
| **Social** | 5-tweet Twitter thread with hook, content, and CTA | GPT-4o-mini |
| **Producer** | 30-second short-form video script (TikTok / Reels style) | GPT-4o-mini |
| **Designer** | Promotional thumbnail image | DALL-E 3 |

Everything is generated in under 60 seconds and displayed in a split-screen UI — blog post on the left, socials and media on the right.

---

## Architecture

```
User enters GitHub repo (owner/repo)
        │
        ▼
┌─────────────────────────────────────────┐
│         Next.js Frontend               │
│   (Azure Static Web Apps — Free tier)  │
└─────────────────┬───────────────────────┘
                  │  POST /api/run?repo=...
                  ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                │
│   (Azure Container Apps — Free tier)   │
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │Copywriter│  │  Social  │            │
│  └──────────┘  └──────────┘            │
│  ┌──────────┐  ┌──────────┐            │
│  │ Producer │  │ Designer │            │
│  └──────────┘  └──────────┘            │
└─────────────────┬───────────────────────┘
                  │
                  ▼
         OpenAI API (GPT-4o-mini + DALL-E 3)
```

---

## Tech Stack

**Frontend**
- [Next.js 16](https://nextjs.org/) with React 19 App Router
- [Tailwind CSS v4](https://tailwindcss.com/) — utility-first styling
- [Framer Motion](https://www.framer.com/motion/) — animations
- [Lucide React](https://lucide.dev/) — icons
- [React Markdown](https://github.com/remarkjs/react-markdown) — renders the generated blog post

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — async Python web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [OpenAI Python SDK v2](https://github.com/openai/openai-python) — GPT-4o-mini + DALL-E 3
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment variable management

**Infrastructure**
- Azure Container Apps — backend (consumption-based free tier, no VM quota)
- Azure Container Registry — Docker image storage
- Azure Static Web Apps — frontend (free tier)
- GitHub Actions — CI/CD, auto-deploys on push to `master`

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
│       ├── page.tsx           # Main UI — input, progress, results
│       ├── layout.tsx         # Root layout and metadata
│       └── globals.css        # Tailwind + custom prose styles
├── Dockerfile                 # Backend container definition
├── requirements.txt           # Python dependencies
└── .github/workflows/
    ├── backend-deploy.yml     # Build + push Docker image → Container Apps
    └── frontend-deploy.yml    # Build + deploy → Static Web Apps
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

Open [http://localhost:3000](http://localhost:3000), enter any GitHub repo (e.g. `vercel/next.js`), and click **Run Pipeline**.

---

## Environment Variables

| Variable | Where | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | Backend | Your OpenAI API key |
| `FRONTEND_URL` | Backend | Allowed CORS origin (your frontend URL) |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API base URL |

---

## Deployment

The project is deployed on Azure using two free-tier services:

| Service | What runs there | Cost |
|---------|----------------|------|
| Azure Container Apps | FastAPI backend (Docker) | Free consumption tier |
| Azure Static Web Apps | Next.js frontend | Free |
| Azure Container Registry | Docker image storage | ~$5/mo (Basic) |

### CI/CD
Every push to `master` triggers automatic deploys:
- Changes to `backend/` or `Dockerfile` → builds Docker image → pushes to ACR → deploys to Container Apps
- Changes to `frontend/` → builds Next.js → deploys to Static Web Apps

GitHub secrets required: `ACR_LOGIN_SERVER`, `ACR_USERNAME`, `ACR_PASSWORD`, `AZURE_CREDENTIALS`, `OPENAI_API_KEY`, `FRONTEND_URL`, `NEXT_PUBLIC_API_URL`.

---

## How to Use

1. Open the [live demo](https://happy-mushroom-0447b8210.7.azurestaticapps.net)
2. Enter a GitHub repository in `owner/repo` format (e.g. `facebook/react`)
3. Click **Run Pipeline**
4. Watch the 4 agents orchestrate in real time (~30–60 seconds)
5. Copy your blog post, Twitter thread, video script, and download the thumbnail
