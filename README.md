# Smart Task Manager

A beginner-friendly task management web app with one AI feature: **Gemini generates a short task description from a task title**.

## Features
- Add tasks with a title and description
- Mark tasks complete / undo completion
- Delete tasks
- Generate task descriptions with Gemini AI

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment (optional but recommended):
   - Windows: `py -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and paste your Gemini API key.
6. Start: `python app.py`
7. Open `http://127.0.0.1:5000`.

The SQLite database `tasks.db` is created automatically. Keep `.env` private; never upload your API key to GitHub.
