import os
import time
from datetime import datetime, timezone

import psycopg2
from flask import Flask, request, render_template, jsonify
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key-change-me")
csrf = CSRFProtect(app)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "dbname": os.environ.get("DB_NAME", "quizdb"),
    "user": os.environ.get("DB_USER", "quizuser"),
    "password": os.environ.get("DB_PASSWORD", "quizpass"),
}

MIN_LENGTH = 8
MAX_LENGTH = 64


def get_conn(retries=5, delay=2):
    last_error = None
    for _ in range(retries):
        try:
            return psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError as exc:
            last_error = exc
            time.sleep(delay)
    raise last_error


def is_common_password(password):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 FROM common_passwords WHERE password = %s LIMIT 1", (password,))
        return cur.fetchone() is not None


def is_password_valid(password):
    if not (MIN_LENGTH <= len(password) <= MAX_LENGTH):
        return False
    if is_common_password(password):
        return False
    return True


def log_new_user(username):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            'INSERT INTO "2301483" (username, created_at) VALUES (%s, %s)',
            (username, datetime.now(timezone.utc)),
        )
        conn.commit()


@csrf.exempt
@app.route("/api/check-password", methods=["POST"])
def check_password():
    data = request.get_json(silent=True) or {}
    return jsonify(valid=is_password_valid(data.get("password", "")))


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not username or not is_password_valid(password):
        return render_template("index.html")
    return render_template("welcome.html", password=password)


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not username or not is_password_valid(password):
        return render_template("register.html")
    log_new_user(username)
    return render_template("welcome.html", password=password)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)