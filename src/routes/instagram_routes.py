from flask import Blueprint, jsonify, request
from src.services.instagram_service import fetch_and_store_instagram_data, \
    get_latest_instagram, get_instagram_statistics, get_instagram_daily_stats
from src.config import Config

instagram_blueprint = Blueprint('instagram', __name__)


@instagram_blueprint.route('/update', methods=['POST'])
def instagram_update():
    fetch_and_store_instagram_data()
    latest = get_latest_instagram()
    return jsonify({"status": "success", "latest": latest})


@instagram_blueprint.route('/latest', methods=['GET'])
def instagram_latest():
    username = request.args.get('username', Config.INSTAGRAM_USERNAME)
    latest = get_latest_instagram(username)
    if latest:
        return jsonify({"platform": "instagram", "latest_data": latest})
    else:
        return jsonify({"platform": "instagram", "message": "Нет данных"}), 404


@instagram_blueprint.route('/statistics', methods=['GET'])
def instagram_statistics():
    username = request.args.get('username', Config.INSTAGRAM_USERNAME)
    stats = get_instagram_statistics(username)
    if stats:
        return jsonify({"username": username, "statistics": stats})
    else:
        return jsonify({"username": username, "message": "Нет данных"}), 404


@instagram_blueprint.route('/daily-stats', methods=['GET'])
def instagram_daily_stats():
    username = request.args.get('username', Config.INSTAGRAM_USERNAME)
    daily_stats = get_instagram_daily_stats(username)
    if daily_stats:
        return jsonify({"username": username, "daily_stats": daily_stats})
    else:
        return jsonify({"username": username, "message": "Нет данных"}), 404
