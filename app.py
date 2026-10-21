from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
import sqlite3
import csv
import io
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
DATABASE = os.path.join(os.path.dirname(__file__), "database.db")
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")  # Change for deployment


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                comments TEXT NOT NULL,
                date_submitted TEXT NOT NULL
            )
        """)
        conn.commit()


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not request.cookies.get("admin_logged_in") == "yes":
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    comments = request.form.get("comments", "").strip()
    try:
        rating = int(request.form.get("rating", ""))
    except (TypeError, ValueError):
        rating = 0

    if not name or not email or not comments or rating not in range(1, 6):
        flash("Please complete every field and choose a rating from 1 to 5.", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        conn.execute(
            "INSERT INTO feedback (name, email, rating, comments, date_submitted) VALUES (?, ?, ?, ?, ?)",
            (name, email, rating, comments, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()

    flash("Thanks! Your feedback has been submitted.", "success")
    return redirect(url_for("index"))


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            response = redirect(url_for("admin_dashboard"))
            response.set_cookie("admin_logged_in", "yes", httponly=True, samesite="Lax")
            return response
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/admin-logout")
def admin_logout():
    response = redirect(url_for("index"))
    response.delete_cookie("admin_logged_in")
    return response


@app.route("/admin-dashboard")
@admin_required
def admin_dashboard():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM feedback ORDER BY date_submitted DESC").fetchall()
        stats = conn.execute(
            "SELECT COUNT(*) AS total, COALESCE(ROUND(AVG(rating), 2), 0) AS average FROM feedback"
        ).fetchone()
        rating_rows = conn.execute("SELECT rating, COUNT(*) AS count FROM feedback GROUP BY rating ORDER BY rating").fetchall()
    rating_counts = {int(row["rating"]): int(row["count"]) for row in rating_rows}
    return render_template("admin.html", feedback=rows, total=stats["total"],
                           average=stats["average"], rating_counts=rating_counts)


@app.route("/api/feedback")
@admin_required
def api_feedback():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM feedback ORDER BY date_submitted DESC").fetchall()
    return jsonify([dict(row) for row in rows])


@app.route("/export-csv")
@admin_required
def export_csv():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM feedback ORDER BY date_submitted DESC").fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "email", "rating", "comments", "date_submitted"])
    for row in rows:
        writer.writerow([row["id"], row["name"], row["email"], row["rating"], row["comments"], row["date_submitted"]])
    return Response("\\ufeff" + output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=feedback.csv"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


init_db()

if __name__ == "__main__":
    app.run(debug=True)
