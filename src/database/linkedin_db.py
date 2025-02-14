import sqlite3
from src.config import Config
from datetime import datetime, timedelta


def add_linkedin_data(profile_id, followers_count):
    with sqlite3.connect(Config.DATABASES['linkedin']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO followers (profile_id, followers_count, timestamp)
            VALUES (?, ?, ?)
        """, (profile_id, followers_count, datetime.now()))
        conn.commit()


def get_latest_linkedin_data(profile_id):
    with sqlite3.connect(Config.DATABASES['linkedin']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT followers_count, timestamp 
            FROM followers 
            WHERE profile_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (profile_id,))
        result = cursor.fetchone()
        return {"count": result[0], "timestamp": result[1]} if result else None


def get_followers_over_period(profile_id, start_time):
    with sqlite3.connect(Config.DATABASES['linkedin']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT followers_count 
            FROM followers 
            WHERE profile_id = ? AND timestamp >= ? 
            ORDER BY timestamp ASC
        """, (profile_id, start_time.strftime('%Y-%m-%d %H:%M:%S')))
        data = cursor.fetchall()
    if len(data) < 2:
        return 0.0
    start_followers = int(str(data[0][0]).replace(',', '').replace(' ', ''))
    end_followers = int(str(data[-1][0]).replace(',', '').replace(' ', ''))
    return round(((end_followers - start_followers) / start_followers) * 100, 2)


def get_daily_followers(profile_id):
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    query = """
        SELECT DATE(timestamp) as date, MAX(followers_count) as followers_count
        FROM followers
        WHERE profile_id = ? AND DATE(timestamp) >= ?
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """
    with sqlite3.connect(Config.DATABASES['linkedin']) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (profile_id, start_date))
        data = cursor.fetchall()

    if data:
        return [{"date": row[0], "followers_count": row[1]} for row in data]
    else:
        return None