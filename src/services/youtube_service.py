from googleapiclient.discovery import build
from src.config import Config
from datetime import datetime, timedelta
from src.database.youtube_db import add_youtube_data, get_latest_youtube_data, get_subscribers_over_period
from src.utils.logger import setup_logger

logger = setup_logger()

def get_youtube_subscribers():
    youtube = build('youtube', 'v3', developerKey=Config.YOUTUBE_API_KEY)
    request = youtube.channels().list(part='statistics', id=Config.YOUTUBE_CHANNEL_ID)
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        subscribers = int(response['items'][0]['statistics']['subscriberCount'])
        logger.info(f"Количество подписчиков YouTube: {subscribers}")
        return subscribers
    logger.warning("Канал не найден или данные недоступны.")
    return None

def fetch_and_store_youtube_data():
    subscribers_count = get_youtube_subscribers()
    if subscribers_count:
        add_youtube_data(Config.YOUTUBE_CHANNEL_ID, subscribers_count)
        logger.info(f"YouTube данные обновлены: {subscribers_count}")
    else:
        logger.warning("Не удалось получить данные YouTube.")

def get_latest_youtube(channel_id=None):
    if channel_id is None:
        channel_id = Config.YOUTUBE_CHANNEL_ID
    return get_latest_youtube_data(channel_id)

def get_youtube_statistics(channel_id):
    periods = {
        "24h": datetime.now() - timedelta(hours=24),
        "week": datetime.now() - timedelta(weeks=1),
        "month": datetime.now() - timedelta(days=30)
    }
    stats = {}
    for period, start_time in periods.items():
        trend = get_subscribers_over_period(channel_id, start_time)
        stats[period] = trend
    return stats
