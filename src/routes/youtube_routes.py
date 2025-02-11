from flask import Blueprint, jsonify, request
from src.services.youtube_service import fetch_and_store_youtube_data, \
    get_latest_youtube, get_youtube_statistics
from src.config import Config

youtube_blueprint = Blueprint('youtube', __name__)


@youtube_blueprint.route('/update', methods=['POST'])
def youtube_update():
    fetch_and_store_youtube_data()
    latest = get_latest_youtube()
    return jsonify({"status": "success", "latest": latest})


@youtube_blueprint.route('/latest', methods=['GET'])
def youtube_latest():
    latest = get_latest_youtube(Config.YOUTUBE_CHANNEL_ID)
    if latest:
        return jsonify({"platform": "youtube", "latest_data": latest})
    else:
        return jsonify({"platform": "youtube", "message": "Нет данных"}), 404


@youtube_blueprint.route('/statistics', methods=['GET'])
def youtube_statistics():
    channel_id = request.args.get('channel_id', Config.YOUTUBE_CHANNEL_ID)
    stats = get_youtube_statistics(channel_id)
    if stats:
        return jsonify({"channel_id": channel_id, "statistics": stats})
    else:
        return jsonify({"channel_id": channel_id, "message": "Нет данных"}), 404

@youtube_blueprint.route('/daily-stats', methods=['GET'])
def youtube_daily_stats():
    from src.services.youtube_service import get_youtube_daily_stats
    channel_id = request.args.get('channel_id', Config.YOUTUBE_CHANNEL_ID)
    daily_stats = get_youtube_daily_stats(channel_id)
    if daily_stats:
        return jsonify({"channel_id": channel_id, "daily_stats": daily_stats})
    else:
        return jsonify({"channel_id": channel_id, "message": "Нет данных"}), 404

