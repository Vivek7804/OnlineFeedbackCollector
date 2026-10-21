# Online Feedback Collector with Admin Dashboard

A Python Flask internship project that collects feedback, stores it in SQLite, and provides an admin dashboard with summary metrics, a rating chart, JSON API, and CSV export.

## Features
- Feedback form: name, email, rating (1–5), comments
- Server-side validation and SQLite storage
- Admin login and dashboard
- Total feedback and average rating
- Rating distribution chart (Chart.js CDN)
- Export feedback as CSV
- JSON endpoint at `/api/feedback` (admin login required)
- Responsive layout

## Requirements
- Python 3.9+
- pip

## Run locally
1. Extract the ZIP.
2. Open a terminal in the `OnlineFeedbackCollector` folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `python -m venv venv` then `venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000`

The SQLite database `database.db` is created automatically on first run.

## Admin login
- URL: `http://127.0.0.1:5000/admin-login`
- Default username: `admin`
- Default password: `admin123`

For deployment, set `ADMIN_USERNAME`, `ADMIN_PASSWORD`, and `SECRET_KEY` environment variables to strong values. This demo uses a simple cookie flag for the admin login and is intended for internship learning/local demonstration, not production deployment. For a real deployment, use Flask sessions, password hashing, CSRF protection, HTTPS, and proper authorization.

## Routes
- `GET /` — feedback form
- `POST /submit-feedback` — validate and save feedback
- `GET /admin-login` / `POST /admin-login` — admin login
- `GET /admin-dashboard` — admin dashboard (login required)
- `GET /admin-logout` — log out admin
- `GET /api/feedback` — JSON feedback list (login required)
- `GET /export-csv` — download CSV (login required)
- `GET /health` — health check

## Project structure
```text
OnlineFeedbackCollector/
├── app.py
├── requirements.txt
├── database.db
├── README.md
├── static/
│   ├── css/style.css
│   └── js/script.js
└── templates/
    ├── layout.html
    ├── index.html
    ├── login.html
    └── admin.html
```
