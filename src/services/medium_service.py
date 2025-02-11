import requests
import re
import json
from src.config import Config
from datetime import datetime, timedelta
from src.database.medium_db import add_medium_data, get_latest_medium_data, get_followers_over_period
from src.utils.logger import setup_logger

logger = setup_logger()

URL = f'https://medium.com/@{Config.MEDIUM_USERNAME}'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def get_followers_apollo(html):
    try:
        apollo_state_pattern = r'<script>window\.__APOLLO_STATE__\s*=\s*({.*?});</script>'
        match = re.search(apollo_state_pattern, html, re.DOTALL)
        if match:
            apollo_data = json.loads(match.group(1))
            user_key = next((k for k in apollo_data if 'User:' in k and f'@{Config.MEDIUM_USERNAME}' in k), None)
            if user_key:
                followers = apollo_data.get(user_key, {}).get('followersCount')
                logger.info(f"Метод Apollo: найдено подписчиков: {followers}")
                return followers
    except Exception as e:
        logger.error(f"Ошибка Apollo метода: {e}")
    logger.warning("Не найден ключ пользователя в Apollo State")
    return None

def get_followers_direct(html):
    try:
        followers_pattern = r'>(\d+)\s+Followers<'
        match = re.search(followers_pattern, html)
        if match:
            followers = int(match.group(1))
            logger.info(f"Прямой поиск: найдено подписчиков: {followers}")
            return followers
    except Exception as e:
        logger.error(f"Ошибка прямого поиска: {e}")
    logger.warning("Прямой поиск не дал результата")
    return None

def get_medium_followers():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        html_content = response.text
        followers = get_followers_apollo(html_content) or get_followers_direct(html_content)
        if followers is not None:
            logger.info(f"Общее количество подписчиков Medium: {followers}")
        else:
            logger.warning("Данные о подписчиках Medium не найдены")
        return followers
    except Exception as e:
        logger.error(f"Общая ошибка при получении данных Medium: {e}")
    return None

def fetch_and_store_medium_data():
    followers_count = get_medium_followers()
    if followers_count is not None:
        add_medium_data(Config.MEDIUM_USERNAME, followers_count)
        logger.info(f"Medium данные обновлены: {followers_count}")
    else:
        logger.warning("Не удалось получить данные Medium.")

def get_latest_medium(username=None):
    if username is None:
        username = Config.MEDIUM_USERNAME
    return get_latest_medium_data(username)

def get_medium_statistics(username):
    periods = {
        "24h": datetime.now() - timedelta(hours=24),
        "week": datetime.now() - timedelta(weeks=1),
        "month": datetime.now() - timedelta(days=30)
    }
    stats = {}
    for period, start_time in periods.items():
        trend = get_followers_over_period(username, start_time)
        stats[period] = trend
    return stats
