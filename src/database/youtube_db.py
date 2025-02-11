import sqlite3
from src.config import Config
from datetime import datetime, timedelta


def add_youtube_data(channel_id, subscribers_count):
    with sqlite3.connect(Config.DATABASES['youtube']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO youtube_followers (channel_id, subscribers_count, timestamp)
            VALUES (?, ?, ?)
        """, (channel_id, subscribers_count, datetime.now()))
        conn.commit()


def get_latest_youtube_data(channel_id):
    with sqlite3.connect(Config.DATABASES['youtube']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT subscribers_count, timestamp 
            FROM youtube_followers 
            WHERE channel_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (channel_id,))
        result = cursor.fetchone()
        return {"count": result[0], "timestamp": result[1]} if result else None


def get_subscribers_over_period(channel_id, start_time):
    with sqlite3.connect(Config.DATABASES['youtube']) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT subscribers_count 
            FROM youtube_followers 
            WHERE channel_id = ? AND timestamp >= ? 
            ORDER BY timestamp ASC
        """, (channel_id, start_time.strftime('%Y-%m-%d %H:%M:%S')))
        data = cursor.fetchall()
    if len(data) < 2:
        return 0.0
    start_subscribers = int(data[0][0])
    end_subscribers = int(data[-1][0])
    return round(
        ((end_subscribers - start_subscribers) / start_subscribers) * 100, 2)


def get_daily_followers(channel_id):
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    query = """
        SELECT DATE(timestamp) as date, MAX(subscribers_count) as subscribers_count
        FROM youtube_followers
        WHERE channel_id = ? AND DATE(timestamp) >= ?
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """
    with sqlite3.connect(Config.DATABASES['youtube']) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (channel_id, start_date))
        data = cursor.fetchall()

    if data:
        return [{"date": row[0], "subscribers_count": row[1]} for row in data]
    else:
        return None
