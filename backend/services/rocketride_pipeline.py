import os
import json
import sqlite3
import subprocess
from pathlib import Path

from rocketride import RocketRideClient
from rocketride.schema import Question

PIPELINES_DIR = Path(__file__).parent.parent.parent / "pipelines"

_ANTIGRAVITY_STATE_DB = Path(os.environ.get("APPDATA", "")) / "Antigravity" / "User" / "globalStorage" / "state.vscdb"
_ENGINE_DIR = Path(os.environ.get("APPDATA", "")) / "Antigravity" / "User" / "globalStorage" / "rocketride.rocketride" / "engines"


def _get_rocketride_apikey() -> str:
    env_key = os.getenv("ROCKETRIDE_APIKEY", "")
    if env_key:
        return env_key
    try:
        conn = sqlite3.connect(str(_ANTIGRAVITY_STATE_DB))
        cur = conn.cursor()
        cur.execute("SELECT value FROM ItemTable WHERE key = 'antigravityAuthStatus'")
        row = cur.fetchone()
        conn.close()
        if row:
            data = json.loads(row[0])
            return data.get("apiKey", "")
    except Exception:
        pass
    return ""


def _get_rocketride_uri() -> str:
    env_uri = os.getenv("ROCKETRIDE_URI", "")
    if env_uri:
        return env_uri
    # Find the active engine PID and look up its listening port
    try:
        for pid_file in _ENGINE_DIR.rglob("engine-*.pid"):
            pid = int(pid_file.read_text().strip())
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if "LISTENING" in line and str(pid) in line.split()[-1:]:
                    parts = line.split()
                    addr = parts[1]  # e.g. 127.0.0.1:55087
                    port = addr.split(":")[-1]
                    return f"http://127.0.0.1:{port}"
    except Exception:
        pass
    return "http://127.0.0.1:5565"


async def run_pipeline(pipe_name: str, prompt: str) -> str:
    """
    Load a .pipe file, start it on the RocketRide engine, send a prompt,
    and return the text answer.
    """
    pipe_path = str(PIPELINES_DIR / f"{pipe_name}.pipe")
    uri = _get_rocketride_uri()
    apikey = _get_rocketride_apikey()

    rr = RocketRideClient(uri=uri)
    await rr.connect(auth=apikey if apikey else None)

    token = None
    try:
        result = await rr.use(filepath=pipe_path)
        token = result["token"]

        question = Question()
        question.addQuestion(prompt)

        response = await rr.chat(token=token, question=question)

        answers = response.get("answers", [])
        return answers[0] if answers else ""
    finally:
        if token:
            try:
                await rr.terminate(token)
            except Exception:
                pass
        await rr.disconnect()
