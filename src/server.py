from flask import Flask, request, jsonify
import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging
import threading
import time

# Импорт функций для получения подписчиков
from linkedin_followers import get_followers_count
from youtube_followers import get_youtube_subscribers
from medium_followers import get_medium_followers  # добавлено для Medium

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Загрузка переменных окружения
load_dotenv()

# Настройки
DEFAULT_PROFILE_ID = os.getenv("PUBLIC_PROFILE_ID", "default_id")
APP_PORT = int(os.getenv("APP_PORT", 8080))
# Путь к chromedriver (укажите корректный путь на вашем сервере)
CHROME_DRIVER_PATH = '/Users/nikogamsahurdia/Downloads/chromedriver/chromedriver'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ------------------ LinkedIn база данных ------------------
DATABASE = 'followers_data.db'

def init_db():
    logging.info("Инициализация базы данных LinkedIn...")
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT NOT NULL,
                followers_count INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    logging.info("База данных LinkedIn инициализирована.")

def add_followers_data(profile_id, followers_count):
    logging.info("Добавление данных для LinkedIn профиля %s: %s подписчиков", profile_id, followers_count)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO followers (profile_id, followers_count) VALUES (?, ?)", (profile_id, followers_count))
        conn.commit()

def get_latest_followers(profile_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT followers_count, timestamp FROM followers WHERE profile_id = ? ORDER BY timestamp DESC LIMIT 1", (profile_id,))
        result = cursor.fetchone()
        if result:
            return {"followers_count": result[0], "timestamp": result[1]}
        return None

def update_linkedin_data():
    try:
        logging.info("Запрос данных о подписчиках для LinkedIn профиля %s...", DEFAULT_PROFILE_ID)
        profile_url = 'https://www.linkedin.com/in/gamsakhurdiya/'
        # Remove driver_path here:
        followers_count = get_followers_count(profile_url, headless=True)
        if followers_count:
            add_followers_data(DEFAULT_PROFILE_ID, followers_count)
            logging.info("Записано количество подписчиков для LinkedIn %s: %s", DEFAULT_PROFILE_ID, followers_count)
        else:
            logging.warning("Информация о подписчиках LinkedIn недоступна.")

        cutoff_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM followers WHERE timestamp < ?", (cutoff_time,))
            deleted = cursor.rowcount
            conn.commit()
        logging.info("Удалено %s записей LinkedIn старше %s", deleted, cutoff_time)
    except Exception as e:
        logging.error("Ошибка при обновлении данных LinkedIn: %s", e)


def linkedin_background_update():
    while True:
        update_linkedin_data()
        time.sleep(3600)  # Обновление каждые 60 минут

# ------------------ YouTube база данных ------------------
YOUTUBE_DB = 'youtube_data.db'

def init_youtube_db():
    logging.info("Инициализация базы данных YouTube...")
    with sqlite3.connect(YOUTUBE_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS youtube_followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL,
                subscribers_count INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    logging.info("База данных YouTube инициализирована.")

def add_youtube_data(channel_id, subscribers_count):
    logging.info("Добавление данных для YouTube канала %s: %s подписчиков", channel_id, subscribers_count)
    with sqlite3.connect(YOUTUBE_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO youtube_followers (channel_id, subscribers_count) VALUES (?, ?)", (channel_id, subscribers_count))
        conn.commit()

def get_latest_youtube(channel_id):
    with sqlite3.connect(YOUTUBE_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT subscribers_count, timestamp FROM youtube_followers WHERE channel_id = ? ORDER BY timestamp DESC LIMIT 1", (channel_id,))
        result = cursor.fetchone()
        if result:
            return {"subscribers_count": result[0], "timestamp": result[1]}
        return None

def update_youtube_data():
    try:
        logging.info("Запрос данных о подписчиках для YouTube канала...")
        subscribers_count = get_youtube_subscribers()
        if subscribers_count:
            channel_id = 'UCRhID0powzDpE4D2KuVKGHg'
            add_youtube_data(channel_id, subscribers_count)
            logging.info("Записано количество подписчиков для YouTube канала %s: %s", channel_id, subscribers_count)
        else:
            logging.warning("Информация о подписчиках YouTube недоступна.")

        cutoff_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(YOUTUBE_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM youtube_followers WHERE timestamp < ?", (cutoff_time,))
            deleted = cursor.rowcount
            conn.commit()
        logging.info("Удалено %s записей YouTube старше %s", deleted, cutoff_time)
    except Exception as e:
        logging.error("Ошибка при обновлении данных YouTube: %s", e)

def youtube_background_update():
    while True:
        update_youtube_data()
        time.sleep(3600)  # Обновление каждые 60 минут

# ------------------ Medium база данных ------------------
MEDIUM_DB = 'medium_data.db'

def init_medium_db():
    logging.info("Инициализация базы данных Medium...")
    with sqlite3.connect(MEDIUM_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medium_followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                followers_count INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    logging.info("База данных Medium инициализирована.")

def add_medium_data(username, followers_count):
    logging.info("Добавление данных для Medium пользователя %s: %s подписчиков", username, followers_count)
    with sqlite3.connect(MEDIUM_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medium_followers (username, followers_count) VALUES (?, ?)", (username, followers_count))
        conn.commit()

def get_latest_medium(username):
    with sqlite3.connect(MEDIUM_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT followers_count, timestamp FROM medium_followers WHERE username = ? ORDER BY timestamp DESC LIMIT 1", (username,))
        result = cursor.fetchone()
        if result:
            return {"followers_count": result[0], "timestamp": result[1]}
        return None

def update_medium_data():
    try:
        logging.info("Запрос данных о подписчиках для Medium пользователя @Eleron...")
        followers_count = get_medium_followers()
        if followers_count is not None:
            username = "Eleron"
            add_medium_data(username, followers_count)
            logging.info("Записано количество подписчиков для Medium пользователя %s: %s", username, followers_count)
        else:
            logging.warning("Информация о подписчиках Medium недоступна.")

        cutoff_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(MEDIUM_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medium_followers WHERE timestamp < ?", (cutoff_time,))
            deleted = cursor.rowcount
            conn.commit()
        logging.info("Удалено %s записей Medium старше %s", deleted, cutoff_time)
    except Exception as e:
        logging.error("Ошибка при обновлении данных Medium: %s", e)

def medium_background_update():
    while True:
        update_medium_data()
        time.sleep(3600)  # Обновление каждые 60 минут

# ------------------ Endpoints ------------------
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "LinkedIn & YouTube & Medium Followers API is running"})

@app.route('/update-now', methods=['POST'])
def update_now():
    try:
        update_linkedin_data()
        latest = get_latest_followers(DEFAULT_PROFILE_ID)
        return jsonify({
            "status": "success",
            "message": "LinkedIn данные обновлены немедленно.",
            "latest": latest
        })
    except Exception as e:
        logging.error("Ошибка в ручном обновлении LinkedIn: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/latest-data', methods=['GET'])
def latest_data():
    profile_id = request.args.get('profile_id', DEFAULT_PROFILE_ID)
    latest = get_latest_followers(profile_id)
    if latest:
        logging.info("Последние данные для LinkedIn профиля %s: %s", profile_id, latest)
        return jsonify({"profile_id": profile_id, "latest_data": latest})
    else:
        logging.warning("Нет данных для LinkedIn профиля %s", profile_id)
        return jsonify({"profile_id": profile_id, "latest_data": {}})

@app.route('/statistics', methods=['GET'])
def statistics():
    profile_id = request.args.get('profile_id', DEFAULT_PROFILE_ID)
    def get_trend_for_period(start_time, end_time):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT followers_count, timestamp FROM followers
                WHERE profile_id = ? AND timestamp BETWEEN ? AND ?
                ORDER BY timestamp ASC
            """, (profile_id, start_time, end_time))
            data = cursor.fetchall()
            if len(data) < 2:
                return 0.0
            # Приведение к int (удаляем запятые и пробелы, если они есть)
            start_followers = int(str(data[0][0]).replace(',', '').replace(' ', ''))
            end_followers = int(str(data[-1][0]).replace(',', '').replace(' ', ''))
            if start_followers > 0:
                trend = ((end_followers - start_followers) / start_followers) * 100
                return round(trend, 2)
            else:
                return 0.0
    now = datetime.now()
    periods = {
        "24h": ((now - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')),
        "week": ((now - timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')),
        "month": ((now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S'))
    }
    stats = {period: get_trend_for_period(start, end) for period, (start, end) in periods.items()}
    logging.info("Статистика трендов для LinkedIn профиля %s: %s", profile_id, stats)
    return jsonify({"profile_id": profile_id, "statistics": stats})

@app.route('/youtube-update', methods=['POST'])
def youtube_update():
    try:
        update_youtube_data()
        latest = get_latest_youtube('UCRhID0powzDpE4D2KuVKGHg')
        return jsonify({
            "status": "success",
            "message": "YouTube данные обновлены немедленно.",
            "latest": latest
        })
    except Exception as e:
        logging.error("Ошибка в ручном обновлении YouTube: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/youtube-latest', methods=['GET'])
def youtube_latest():
    channel_id = request.args.get('channel_id', 'UCRhID0powzDpE4D2KuVKGHg')
    latest = get_latest_youtube(channel_id)
    if latest:
        logging.info("Последние данные для YouTube канала %s: %s", channel_id, latest)
        return jsonify({"channel_id": channel_id, "latest_data": latest})
    else:
        logging.warning("Нет данных для YouTube канала %s", channel_id)
        return jsonify({"channel_id": channel_id, "latest_data": {}})

@app.route('/medium-update', methods=['POST'])
def medium_update():
    try:
        update_medium_data()
        latest = get_latest_medium("Eleron")
        return jsonify({
            "status": "success",
            "message": "Medium данные обновлены немедленно.",
            "latest": latest
        })
    except Exception as e:
        logging.error("Ошибка в ручном обновлении Medium: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/medium-latest', methods=['GET'])
def medium_latest():
    username = request.args.get('username', 'Eleron')
    latest = get_latest_medium(username)
    if latest:
        logging.info("Последние данные для Medium пользователя %s: %s", username, latest)
        return jsonify({"username": username, "latest_data": latest})
    else:
        logging.warning("Нет данных для Medium пользователя %s", username)
        return jsonify({"username": username, "latest_data": {}})

if __name__ == "__main__":
    init_db()
    init_youtube_db()
    init_medium_db()
    linkedin_thread = threading.Thread(target=linkedin_background_update, daemon=True)
    linkedin_thread.start()
    youtube_thread = threading.Thread(target=youtube_background_update, daemon=True)
    youtube_thread.start()
    medium_thread = threading.Thread(target=medium_background_update, daemon=True)
    medium_thread.start()
    logging.info("Запуск сервера на порту %s...", APP_PORT)
    app.run(host="0.0.0.0", port=APP_PORT)
