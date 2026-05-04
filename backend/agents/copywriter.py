import json
from openai import OpenAI


def write_blog_post(client: OpenAI, issues: list, repo_name: str) -> str:
    """
    Takes cleaned GitHub issue data and drafts a weekly community blog post.
    Returns raw markdown text.
    """
    issue_summary = json.dumps(issues, indent=2)

    prompt = f"""You are a developer advocate writing a weekly community update 
for the open-source project "{repo_name}".

Below is this week's GitHub issue activity (JSON). Use it to write a short, 
energetic blog post in markdown. Keep it under 500 words.

Structure:
- A catchy title
- A one-paragraph intro welcoming the community
- "Highlights This Week" section covering the most interesting 2-3 issues
- "Bugs & Fixes" section summarizing closed issues
- "Join the Conversation" section linking to the most active open discussions
- A closing paragraph encouraging contributions

Use the actual issue titles and URLs from the data. Write like a real human dev 
advocate — conversational, not corporate. No fluff.

Issue data:
{issue_summary}"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write concise, authentic developer community updates. No corporate speak."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return resp.choices[0].message.content
