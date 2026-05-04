import json
from openai import OpenAI


def write_video_script(client: OpenAI, issues: list, repo_name: str) -> str:
    """
    Generates a short-form video script (TikTok/Reels style)
    based on the week's most interesting community activity.
    """
    issue_summary = json.dumps(issues, indent=2)

    prompt = f"""Write a 30-second short-form video script for TikTok/YouTube Shorts 
about the open-source project "{repo_name}".

Pick the single most interesting issue or feature from the data below and 
build the script around it.

Format:
HOOK (0-3s): A punchy one-liner to stop the scroll
CONTEXT (3-12s): What the project is and why this matters
THE STORY (12-25s): What happened this week — the bug, the fix, the discussion
CTA (25-30s): Tell viewers to check out the repo

Keep it casual and developer-focused. Write the actual spoken words, 
not stage directions. Include [B-ROLL] notes for visual suggestions.

Issue data:
{issue_summary}"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write viral short-form video scripts for developer audiences."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )

    return resp.choices[0].message.content
