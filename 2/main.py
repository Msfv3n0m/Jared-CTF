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
    if '--' in name or ' select ' in name.lower():
        return jsonify({"error": "Invalid input"}), 400
    else:
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

    # --- Create users table ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)
    print("Table 'users' ready.")

    # Insert sample users
    sample_users = [
        ("Alice", "alice@example.com"),
        ("Bob", "bob@example.com")
    ]
    cur.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)", sample_users)

    # --- Create customers table ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        postal_code TEXT,
        country TEXT DEFAULT 'USA',
        created_at TEXT DEFAULT (datetime('now')),
        last_order_amount REAL DEFAULT 0.0,
        total_spend REAL DEFAULT 0.0,
        vip INTEGER DEFAULT 0,
        preferences TEXT,
        notes TEXT
    )
    """)
    print("Table 'customers' ready.")

    # Insert sample customers
    customers = [
        ("Ava", "Morrison", "ava.morrison@example.com", "+1-317-555-0101", "12 Maple St", "Indianapolis", "IN", "46204", "USA",
         "2024-06-14 10:12:00", 89.99, 340.47, 0, '{"newsletter":true,"categories":["home","garden"]}', "Prefers email invoice"),
        ("Liam", "Chen", "liam.chen@example.net", "+1-212-555-0192", "404 Park Ave", "New York", "NY", "10022", "USA",
         "2023-11-02 15:45:00", 250.00, 1250.00, 1, '{"newsletter":false,"categories":["electronics"]}', "VIP since 2024-03"),
        ("Sophia", "Garcia", "sophia.garcia@example.org", "+44 20 7946 0958", "Flat 3, 8 Baker St",
         "London", "", "W1U1AA", "UK", "2025-01-09 09:03:00", 19.50, 45.25, 0, '{"newsletter":true}', ""),
        ("Noah", "Patel", "noah.patel@example.com", "+91-80-5555-1212", "22 MG Road", "Bengaluru", "KA",
         "560001", "India", "2022-08-30 20:20:00", 499.99, 499.99, 1, '{"gift_wrap":true}', "Corporate contact")
    ]

    cur.executemany("""
    INSERT INTO customers (
        first_name, last_name, email, phone, address, city, state, postal_code, country,
        created_at, last_order_amount, total_spend, vip, preferences, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers)

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
