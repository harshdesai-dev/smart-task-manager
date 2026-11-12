import os, sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "local-development-key")
DB = os.path.join(os.path.dirname(__file__), "tasks.db")

def connect():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            completed INTEGER DEFAULT 0
        )""")

def ask_gemini(prompt):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("Add your Gemini API key to the .env file.")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    response = requests.post(
        url, params={"key": key},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=25
    )
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()

@app.route("/")
def index():
    with connect() as con:
        tasks = con.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return render_template("index.html", tasks=tasks)

@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    if title:
        with connect() as con:
            con.execute("INSERT INTO tasks(title, description) VALUES (?, ?)", (title, description))
    return redirect(url_for("index"))

@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    with connect() as con:
        con.execute("UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id=?", (task_id,))
    return redirect(url_for("index"))

@app.post("/delete/<int:task_id>")
def delete(task_id):
    with connect() as con:
        con.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    return redirect(url_for("index"))

@app.post("/ai-description")
def ai_description():
    title = request.json.get("title", "").strip()
    if not title:
        return jsonify(error="Enter a task title first."), 400
    try:
        result = ask_gemini(
            "Write a clear, practical 2-3 sentence description for this task. "
            "Include a useful next action. Do not add a heading. Task: " + title
        )
        return jsonify(description=result)
    except Exception as e:
        return jsonify(error=f"AI request failed: {e}"), 502

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
