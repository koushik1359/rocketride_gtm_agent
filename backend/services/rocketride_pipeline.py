import os
from pathlib import Path

from rocketride import RocketRideClient
from rocketride.schema import Question

PIPELINES_DIR = Path(__file__).parent.parent.parent / "pipelines"
ROCKETRIDE_URI = os.getenv("ROCKETRIDE_URI", "http://localhost:55087")
ROCKETRIDE_APIKEY = os.getenv("ROCKETRIDE_APIKEY", "")


async def run_pipeline(pipe_name: str, prompt: str) -> str:
    """
    Load a .pipe file, start it on the RocketRide engine, send a prompt,
    and return the text answer.
    """
    pipe_path = str(PIPELINES_DIR / f"{pipe_name}.pipe")

    rr = RocketRideClient(uri=ROCKETRIDE_URI)
    await rr.connect(ROCKETRIDE_APIKEY)

    try:
        result = await rr.use(filepath=pipe_path)
        token = result["token"]

        question = Question()
        question.addQuestion(prompt)

        response = await rr.chat(token=token, question=question)

        answers = response.get("answers", [])
        return answers[0] if answers else ""
    finally:
        await rr.disconnect()
