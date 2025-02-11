from flask import Flask, jsonify, request
from src.services.linkedin_service import (
    fetch_and_store_linkedin_data, get_latest_linkedin, get_linkedin_statistics
)
from src.services.youtube_service import (
    fetch_and_store_youtube_data, get_latest_youtube, get_youtube_statistics
)
from src.services.medium_service import (
    fetch_and_store_medium_data, get_latest_medium, get_medium_statistics
)
from src.config import Config
from src.utils.logger import setup_logger
import threading
import time

logger = setup_logger()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Фоновые задачи
def linkedin_background_update():
    while True:
        fetch_and_store_linkedin_data()
        time.sleep(3600)

def youtube_background_update():
    while True:
        fetch_and_store_youtube_data()
        time.sleep(3600)

def medium_background_update():
    while True:
        fetch_and_store_medium_data()
        time.sleep(3600)

# API Endpoints
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Followers API is running"})

# LinkedIn Endpoints
@app.route('/linkedin-update', methods=['POST'])
def linkedin_update():
    fetch_and_store_linkedin_data()
    latest = get_latest_linkedin()
    return jsonify({"status": "success", "latest": latest})

@app.route('/linkedin-latest', methods=['GET'])
def linkedin_latest():
    profile_id = request.args.get('profile_id', Config.LINKEDIN_PROFILE_ID)
    latest = get_latest_linkedin(profile_id)
    if latest:
        return jsonify({"platform": "linkedin", "profile_id": profile_id, "latest_data": latest})
    else:
        return jsonify({"platform": "linkedin", "profile_id": profile_id, "message": "Нет данных"}), 404

@app.route('/statistics', methods=['GET'])
def linkedin_statistics():
    profile_id = request.args.get('profile_id', Config.LINKEDIN_PROFILE_ID)
    stats = get_linkedin_statistics(profile_id)
    if stats:
        return jsonify({"profile_id": profile_id, "statistics": stats})
    else:
        return jsonify({"profile_id": profile_id, "message": "Нет данных"}), 404

# YouTube Endpoints
@app.route('/youtube-update', methods=['POST'])
def youtube_update():
    fetch_and_store_youtube_data()
    latest = get_latest_youtube()
    return jsonify({"status": "success", "latest": latest})

@app.route('/youtube-latest', methods=['GET'])
def youtube_latest():
    latest = get_latest_youtube(Config.YOUTUBE_CHANNEL_ID)
    if latest:
        return jsonify({"platform": "youtube", "latest_data": latest})
    else:
        return jsonify({"platform": "youtube", "message": "Нет данных"}), 404

@app.route('/youtube-statistics', methods=['GET'])
def youtube_statistics():
    channel_id = request.args.get('channel_id', Config.YOUTUBE_CHANNEL_ID)
    stats = get_youtube_statistics(channel_id)
    if stats:
        return jsonify({"channel_id": channel_id, "statistics": stats})
    else:
        return jsonify({"channel_id": channel_id, "message": "Нет данных"}), 404

# Medium Endpoints
@app.route('/medium-update', methods=['POST'])
def medium_update():
    fetch_and_store_medium_data()
    latest = get_latest_medium()
    return jsonify({"status": "success", "latest": latest})

@app.route('/medium-latest', methods=['GET'])
def medium_latest():
    latest = get_latest_medium(Config.MEDIUM_USERNAME)
    if latest:
        return jsonify({"platform": "medium", "latest_data": latest})
    else:
        return jsonify({"platform": "medium", "message": "Нет данных"}), 404

@app.route('/medium-statistics', methods=['GET'])
def medium_statistics():
    username = request.args.get('username', Config.MEDIUM_USERNAME)
    stats = get_medium_statistics(username)
    if stats:
        return jsonify({"username": username, "statistics": stats})
    else:
        return jsonify({"username": username, "message": "Нет данных"}), 404

if __name__ == "__main__":
    threading.Thread(target=linkedin_background_update, daemon=True).start()
    threading.Thread(target=youtube_background_update, daemon=True).start()
    threading.Thread(target=medium_background_update, daemon=True).start()
    logger.info(f"Запуск сервера на порту {Config.APP_PORT}...")
    app.run(host="0.0.0.0", port=Config.APP_PORT)
