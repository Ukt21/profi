import sqlite3
from datetime import datetime, timedelta
from ..settings import DB_PATH, PROMO_VALID_DAYS

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            rating INTEGER,
            comment TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS promo(
            code TEXT PRIMARY KEY,
            user_id INTEGER,
            discount INTEGER,
            expires_at TEXT,
            used INTEGER DEFAULT 0
        );
        """)
        con.commit()

def save_feedback(user_id:int, username:str|None, rating:int, comment:str|None):
    with get_conn() as con:
        con.execute("""
            INSERT INTO feedback(user_id, username, rating, comment) VALUES(?,?,?,?)
        """, (user_id, username, rating, comment))
        con.commit()

def create_promo(code:str, user_id:int, discount:int=10):
    expires = (datetime.utcnow() + timedelta(days=PROMO_VALID_DAYS)).isoformat()
    with get_conn() as con:
        con.execute("""
            INSERT OR REPLACE INTO promo(code, user_id, discount, expires_at) VALUES(?,?,?,?)
        """, (code, user_id, discount, expires))
        con.commit()

def get_stats():
    with get_conn() as con:
        cur = con.cursor()
        cur.execute("""SELECT COUNT(*), AVG(rating) FROM feedback""")
        total, avg = cur.fetchone()
        return {"total": total or 0, "avg": round(avg, 2) if avg else 0.0}

def export_feedback_csv(path:str):
    import csv
    with get_conn() as con, open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id","user_id","username","rating","comment","created_at")
]
        for row in con.execute("SELECT id,user_id,username,rating,comment,created_at FROM feedback ORDER BY id DESC"):
            writer.writerow(row)
