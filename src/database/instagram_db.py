import sqlite3
from src.config import Config
from datetime import datetime, timedelta


def add_instagram_data(username, followers_count):
    with sqlite3.connect(Config.DATABASES['instagram']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS instagram_followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                followers_count INTEGER NOT NULL,
                timestamp DATETIME NOT NULL
            )
        """)
        cursor.execute("""
            INSERT INTO instagram_followers (username, followers_count, timestamp)
            VALUES (?, ?, ?)
        """, (username, followers_count, datetime.now()))
        conn.commit()


def get_latest_instagram_data(username):
    with sqlite3.connect(Config.DATABASES['instagram']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT followers_count, timestamp 
            FROM instagram_followers 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (username,))
        result = cursor.fetchone()
        return {"count": result[0], "timestamp": result[1]} if result else None


def get_subscribers_over_period(username, start_time):
    with sqlite3.connect(Config.DATABASES['instagram']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT followers_count 
            FROM instagram_followers 
            WHERE username = ? AND timestamp >= ? 
            ORDER BY timestamp ASC
        """, (username, start_time.strftime('%Y-%m-%d %H:%M:%S')))
        data = cursor.fetchall()
    if len(data) < 2:
        return 0.0
    start_followers = int(data[0][0])
    end_followers = int(data[-1][0])
    return round(
        ((end_followers - start_followers) / start_followers) * 100, 2)


def get_daily_followers(username):
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    query = """
        SELECT DATE(timestamp) as date, MAX(followers_count) as followers_count
        FROM instagram_followers
        WHERE username = ? AND DATE(timestamp) >= ?
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """
    with sqlite3.connect(Config.DATABASES['instagram']) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (username, start_date))
        data = cursor.fetchall()

    if data:
        return [{"date": row[0], "followers_count": row[1]} for row in data]
    else:
        return None 