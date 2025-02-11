import sqlite3
from src.config import Config
from datetime import datetime

def add_medium_data(username, followers_count):
    with sqlite3.connect(Config.DATABASES['medium']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medium_followers (username, followers_count, timestamp)
            VALUES (?, ?, ?)
        """, (username, followers_count, datetime.now()))
        conn.commit()

def get_latest_medium_data(username):
    with sqlite3.connect(Config.DATABASES['medium']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT followers_count, timestamp 
            FROM medium_followers 
            WHERE username = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (username,))
        result = cursor.fetchone()
        return {"count": result[0], "timestamp": result[1]} if result else None

def get_followers_over_period(username, start_time):
    with sqlite3.connect(Config.DATABASES['medium']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT followers_count 
            FROM medium_followers 
            WHERE username = ? AND timestamp >= ? 
            ORDER BY timestamp ASC
        """, (username, start_time.strftime('%Y-%m-%d %H:%M:%S')))
        data = cursor.fetchall()
    if len(data) < 2:
        return 0.0
    start_followers = int(data[0][0])
    end_followers = int(data[-1][0])
    return round(((end_followers - start_followers) / start_followers) * 100, 2)
