from flask import Flask
from src.routes.linkedin_routes import linkedin_blueprint
from src.routes.youtube_routes import youtube_blueprint
from src.routes.medium_routes import medium_blueprint
from src.config import Config
from src.utils.logger import setup_logger
import threading
import time

logger = setup_logger()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Регистрация Blueprint для каждого сервиса
app.register_blueprint(linkedin_blueprint, url_prefix='/linkedin')
app.register_blueprint(youtube_blueprint, url_prefix='/youtube')
app.register_blueprint(medium_blueprint, url_prefix='/medium')


# Фоновые задачи
def linkedin_background_update():
    while True:
        from src.services.linkedin_service import fetch_and_store_linkedin_data
        fetch_and_store_linkedin_data()
        time.sleep(3600)


def youtube_background_update():
    while True:
        from src.services.youtube_service import fetch_and_store_youtube_data
        fetch_and_store_youtube_data()
        time.sleep(3600)


def medium_background_update():
    while True:
        from src.services.medium_service import fetch_and_store_medium_data
        fetch_and_store_medium_data()
        time.sleep(3600)


if __name__ == "__main__":
    threading.Thread(target=linkedin_background_update, daemon=True).start()
    threading.Thread(target=youtube_background_update, daemon=True).start()
    threading.Thread(target=medium_background_update, daemon=True).start()
    logger.info(f"Запуск сервера на порту {Config.APP_PORT}...")
    app.run(host="0.0.0.0", port=Config.APP_PORT)
