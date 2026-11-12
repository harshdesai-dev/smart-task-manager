# Smart Task Manager

A task management web application with Gemini AI-powered task description generation.

## Features
- Add, edit and delete tasks
- Mark tasks complete or pending
- Filter tasks
- Save tasks using browser LocalStorage
- Generate task descriptions using Gemini AI
- Responsive dark-themed interface

## Technology Stack
- Python
- Flask
- HTML, CSS and JavaScript
- Google Gemini API
- Browser LocalStorage

## Local Setup

1. Create virtual environment:
   python -m venv venv

2. Activate:
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Configure environment variables in .env:
   GEMINI_API_KEY=your_api_key
   GEMINI_MODEL=your_model
   FLASK_SECRET_KEY=your_secret

5. Run:
   python app.py

6. Open http://127.0.0.1:5000

## Deployment

Production server: Gunicorn

Configure GEMINI_API_KEY, GEMINI_MODEL and FLASK_SECRET_KEY
as environment variables in your hosting provider.

Tasks are stored locally in the user's browser.
They are not synchronized between devices.

Never commit your .env file or API keys.
