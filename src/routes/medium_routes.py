from flask import Blueprint, jsonify, request
from src.services.medium_service import fetch_and_store_medium_data, \
    get_latest_medium, get_medium_statistics
from src.config import Config

medium_blueprint = Blueprint('medium', __name__)


@medium_blueprint.route('/update', methods=['POST'])
def medium_update():
    fetch_and_store_medium_data()
    latest = get_latest_medium()
    return jsonify({"status": "success", "latest": latest})


@medium_blueprint.route('/latest', methods=['GET'])
def medium_latest():
    latest = get_latest_medium(Config.MEDIUM_USERNAME)
    if latest:
        return jsonify({"platform": "medium", "latest_data": latest})
    else:
        return jsonify({"platform": "medium", "message": "Нет данных"}), 404


@medium_blueprint.route('/statistics', methods=['GET'])
def medium_statistics():
    username = request.args.get('username', Config.MEDIUM_USERNAME)
    stats = get_medium_statistics(username)
    if stats:
        return jsonify({"username": username, "statistics": stats})
    else:
        return jsonify({"username": username, "message": "Нет данных"}), 404

@medium_blueprint.route('/daily-stats', methods=['GET'])
def medium_daily_stats():
    from src.services.medium_service import get_medium_daily_stats
    username = request.args.get('username', Config.MEDIUM_USERNAME)
    daily_stats = get_medium_daily_stats(username)
    if daily_stats:
        return jsonify({"username": username, "daily_stats": daily_stats})
    else:
        return jsonify({"username": username, "message": "Нет данных"}), 404

