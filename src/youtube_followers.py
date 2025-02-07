from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_CHANNEL")
CHANNEL_ID = 'UCRhID0powzDpE4D2KuVKGHg'

def get_youtube_subscribers():
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.channels().list(
        part='statistics',
        id=CHANNEL_ID
    )
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        subscribers = response['items'][0]['statistics']['subscriberCount']
        return subscribers
    else:
        return None

if __name__ == "__main__":
    subscribers = get_youtube_subscribers()
    if subscribers:
        print(f"Количество подписчиков: {subscribers}")
    else:
        print("Канал не найден или данные недоступны.")
