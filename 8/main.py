from flask import Flask, request, jsonify, make_response
import bcrypt
import sqlite3
import os.path
import secrets

DB_FILE = "db.sqlite3"

LOGIN_TEMPLATE = """
<form method="POST">
  <input name="username" placeholder="Username">
  <input name="password" type="password" placeholder="Password">
  <button type="submit">Login</button>
</form>
"""

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return make_response(LOGIN_TEMPLATE, 200)
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("select * from users where username = ?", (username,))
        data = cur.fetchone()
        if data is None:
            response = make_response('invalid credentials', 401)
        elif len(data) == 0:
            response = make_response('invalid credentials', 401)
        else:
            if bcrypt.checkpw(password.encode("utf-8"), data['password_hash']):
                session_token = secrets.token_urlsafe(32)
                cur.execute(
                    "update users set session_token = ? where username = ?", (session_token, username))
                conn.commit()
                response = make_response(session_token + '\n', 200)
                response.set_cookie('session', session_token,
                                samesite='None', secure=True)
            else:
                response = make_response('invalid credentials', 401)
        cur.close()
        conn.close()
        return add_cors_headers(response)

@app.route("/get_session", methods=["GET", "OPTIONS"])
def get_session():
    response = make_response()
    if request.method == "GET":
        session = request.cookies.get('session')
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "select session_token from users where session_token = ?", (session,))
        data = cur.fetchone()
        if data is None:
            response = make_response('invalid session', 401)
        else:
            response = make_response(session + '\n', 200)
        cur.close()
        conn.close()
    return add_cors_headers(response)


def setup_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash BLOB NOT NULL,
            session_token TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Table 'users' ready.")

    users = [
        ("alice", "S3cureP@ssw0rd"),
        ("bob",   "another-secret")
    ]

    for username, plain_pw in users:
        pw_hash = hash_password(plain_pw)
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, pw_hash)
            )
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists — skipping insert.")

    conn.commit()
    cur.close()
    conn.close()


def hash_password(plain_password: str) -> bytes:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())


if __name__ == "__main__":
    setup_db()
    with open('README', 'r') as f:
        print(f"\033[32mGOAL: {f.read()}\033[0m")
    app.run(host='0.0.0.0', ssl_context=("cert.pem", "key.pem"))
