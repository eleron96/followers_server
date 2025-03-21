from instagrapi import Client
from src.config import Config
from datetime import datetime, timedelta
from src.database.instagram_db import add_instagram_data, get_latest_instagram_data, \
    get_subscribers_over_period
from src.utils.logger import setup_logger
from src.database.instagram_db import get_daily_followers
import time
import os
import random

logger = setup_logger()

def get_instagram_subscribers():
    try:
        logger.info("Создаем новый клиент Instagram...")
        client = Client()
        
        logger.info("Попытка авторизации в Instagram...")
        client.login(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD)
        logger.info("Успешная авторизация в Instagram")
            
        logger.info("Получаем user_id...")
        user_id = client.user_id_from_username(Config.INSTAGRAM_USERNAME)
        logger.info(f"Получен user_id: {user_id}")
        
        logger.info("Запрашиваем информацию о пользователе...")
        user_info = client.user_info(user_id)
        followers_count = user_info.follower_count
        logger.info(f"Количество подписчиков Instagram: {followers_count}")
        
        return followers_count
    except Exception as e:
        logger.error(f"Ошибка при получении данных Instagram: {str(e)}")
        # Если это ошибка JSONDecodeError, пробуем еще раз
        if "JSONDecodeError" in str(e):
            logger.info("Повторная попытка после JSONDecodeError...")
            try:
                time.sleep(2)  # Небольшая задержка
                user_info = client.user_info(user_id)
                followers_count = user_info.follower_count
                logger.info(f"Количество подписчиков Instagram (повторная попытка): {followers_count}")
                return followers_count
            except Exception as retry_error:
                logger.error(f"Ошибка при повторной попытке: {str(retry_error)}")
        return None

def fetch_and_store_instagram_data():
    followers_count = get_instagram_subscribers()
    if followers_count:
        # Всегда сохраняем данные, даже если количество не изменилось
        add_instagram_data(Config.INSTAGRAM_USERNAME, followers_count)
        logger.info(f"Instagram данные обновлены: {followers_count}")
        return {"count": followers_count, "timestamp": datetime.now().isoformat()}
    else:
        logger.warning("Не удалось получить данные Instagram.")
        return None

def get_latest_instagram(username=None):
    if username is None:
        username = Config.INSTAGRAM_USERNAME
    return get_latest_instagram_data(username)

def get_instagram_statistics(username):
    periods = {
        "24h": datetime.now() - timedelta(hours=24),
        "week": datetime.now() - timedelta(weeks=1),
        "month": datetime.now() - timedelta(days=30)
    }
    stats = {}
    for period, start_time in periods.items():
        trend = get_subscribers_over_period(username, start_time)
        stats[period] = trend
    return stats

def get_instagram_daily_stats(username):
    return get_daily_followers(username)
