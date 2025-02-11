from flask import Blueprint, jsonify, request
from src.services.linkedin_service import fetch_and_store_linkedin_data, \
    get_latest_linkedin, get_linkedin_statistics
from src.config import Config

linkedin_blueprint = Blueprint('linkedin', __name__)


@linkedin_blueprint.route('/update', methods=['POST'])
def linkedin_update():
    fetch_and_store_linkedin_data()
    latest = get_latest_linkedin()
    return jsonify({"status": "success", "latest": latest})


@linkedin_blueprint.route('/latest', methods=['GET'])
def linkedin_latest():
    profile_id = request.args.get('profile_id', Config.LINKEDIN_PROFILE_ID)
    latest = get_latest_linkedin(profile_id)
    if latest:
        return jsonify({"platform": "linkedin", "profile_id": profile_id,
                        "latest_data": latest})
    else:
        return jsonify({"platform": "linkedin", "profile_id": profile_id,
                        "message": "Нет данных"}), 404


@linkedin_blueprint.route('/statistics', methods=['GET'])
def linkedin_statistics():
    profile_id = request.args.get('profile_id', Config.LINKEDIN_PROFILE_ID)
    stats = get_linkedin_statistics(profile_id)
    if stats:
        return jsonify({"profile_id": profile_id, "statistics": stats})
    else:
        return jsonify({"profile_id": profile_id, "message": "Нет данных"}), 404

@linkedin_blueprint.route('/daily-stats', methods=['GET'])
def linkedin_daily_stats():
    from src.services.linkedin_service import get_linkedin_daily_stats
    profile_id = request.args.get('profile_id', Config.LINKEDIN_PROFILE_ID)
    daily_stats = get_linkedin_daily_stats(profile_id)
    if daily_stats:
        return jsonify({"profile_id": profile_id, "daily_stats": daily_stats})
    else:
        return jsonify({"profile_id": profile_id, "message": "Нет данных"}), 404

