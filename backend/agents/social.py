import json
from openai import OpenAI


def write_twitter_thread(client: OpenAI, issues: list, repo_name: str) -> str:
    """
    Generates a 5-tweet thread highlighting this week's community activity.
    Returns the thread as numbered text.
    """
    issue_summary = json.dumps(issues, indent=2)

    prompt = f"""Write a 5-tweet thread for X (Twitter) about this week's 
community activity on the open-source project "{repo_name}".

Rules:
- Tweet 1: Hook — something attention-grabbing about the project's momentum
- Tweets 2-4: Each highlights one interesting issue or discussion, include the URL
- Tweet 5: CTA — invite developers to star the repo and contribute
- Each tweet must be under 280 characters
- Use 1-2 relevant emojis per tweet, don't overdo it
- Write like an excited developer, not a marketing intern
- Number each tweet like "1/" "2/" etc.

Issue data:
{issue_summary}"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You write punchy, authentic dev tweets. No hashtag spam."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )

    return resp.choices[0].message.content
