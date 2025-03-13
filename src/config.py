import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_PORT = int(os.getenv("APP_PORT", 8080))
    LINKEDIN_PROFILE_ID = os.getenv("PUBLIC_PROFILE_ID", "default_id")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_CHANNEL")
    YOUTUBE_CHANNEL_ID = 'UCRhID0powzDpE4D2KuVKGHg'
    MEDIUM_USERNAME = 'Eleron'
    INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

    DATABASES = {
        'linkedin': '/var/lib/followers_data/followers_data.db',
        'youtube': '/var/lib/followers_data/youtube_data.db',
        'medium': '/var/lib/followers_data/medium_data.db',
        'instagram': '/var/lib/followers_data/instagram_data.db',
    }
