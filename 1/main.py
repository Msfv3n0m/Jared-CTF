from flask import Flask, request, jsonify
import sqlite3
import os

DB_FILE = "db.sqlite3"

app = Flask(__name__)


@app.route("/users", methods=["GET", "POST"])
def users():
    name = request.args.get('name')
    if name == None:
        return jsonify({})
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM users WHERE name = '{name}'")
    rows = cur.fetchall()
    users = [dict(row) for row in rows]
    cur.close()
    conn.close()
    return jsonify({"users": users})


def setup_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)
    print("Table 'users' ready.")

    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                ("Alice", "alice@example.com"))
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                ("Bob", "bob@example.com"))
    conn.commit()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    print("Users in DB:")
    for row in rows:
        print(dict(row))

    cur.close()
    conn.close()


if __name__ == "__main__":
    if not os.path.isfile(DB_FILE):
        setup_db()
    with open('README', 'r') as f:
        print(f"\033[32mGOAL: {f.read()}\033[0m")
    app.run(host='0.0.0.0')
