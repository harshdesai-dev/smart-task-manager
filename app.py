
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)

# Security configuration
app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is missing from the .env file.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "").strip()


def ask_gemini(prompt):
    """Generate a response using the Gemini API."""

    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key is not configured.")

    if not GEMINI_MODEL:
        raise ValueError("Gemini model is not configured.")

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{GEMINI_MODEL}:generateContent"
    )

    response = requests.post(
        url,
        params={"key": GEMINI_API_KEY},
        json={
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        },
        timeout=30
    )

    if not response.ok:
        app.logger.error(
            "Gemini API returned HTTP %s",
            response.status_code
        )
        raise RuntimeError(
            f"Gemini API request failed (HTTP {response.status_code})."
        )

    data = response.json()

    candidates = data.get("candidates", [])

    if not candidates:
        raise RuntimeError(
            "Gemini did not generate a response. Try another prompt."
        )

    parts = candidates[0].get("content", {}).get("parts", [])

    result = " ".join(
        part.get("text", "")
        for part in parts
        if part.get("text")
    ).strip()

    if not result:
        raise RuntimeError("Gemini returned an empty response.")

    return result


@app.route("/")
def index():
    # Tasks will be loaded and displayed by browser LocalStorage.
    return render_template("index.html")


@app.route("/ai-description", methods=["POST"])
def ai_description():
    data = request.get_json(silent=True) or {}

    title = data.get("title", "")

    if not isinstance(title, str):
        return jsonify(error="Invalid task title."), 400

    title = title.strip()

    if not title:
        return jsonify(error="Enter a task title first."), 400

    if len(title) > 200:
        return jsonify(error="Task title must be under 200 characters."), 400

    prompt = (
        "Write a clear, practical 2-3 sentence description for this task. "
        "Include a useful next action. Do not add a heading. "
        f"Task: {title}"
    )

    try:
        result = ask_gemini(prompt)
        return jsonify(description=result)

    except ValueError as error:
        return jsonify(error=str(error)), 503

    except Exception:
        app.logger.exception("AI description generation failed.")
        return jsonify(
            error="AI request failed. Check your API configuration and try again."
        ), 502


@app.route("/health")
def health():
    return jsonify(
        status="ok",
        application="Smart Task Manager",
        database="disabled",
        ai_configured=bool(GEMINI_API_KEY and GEMINI_MODEL)
    )


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode)
