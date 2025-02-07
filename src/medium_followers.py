import requests
import re
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# URL страницы Medium пользователя
URL = 'https://medium.com/@Eleron'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_followers_apollo(html):
    """Парсинг через Apollo State"""
    try:
        apollo_state_pattern = r'<script>window\.__APOLLO_STATE__\s*=\s*({.*?});</script>'
        match = re.search(apollo_state_pattern, html, re.DOTALL)
        if not match:
            logging.warning("Не найден Apollo State в HTML")
            return None
        apollo_data = json.loads(match.group(1))
        user_key = next((k for k in apollo_data if 'User:' in k and '@Eleron' in k), None)
        if user_key:
            followers = apollo_data.get(user_key, {}).get('followersCount')
            logging.info("Метод Apollo: найдено подписчиков: %s", followers)
            return followers
        else:
            logging.warning("Не найден ключ пользователя в Apollo State")
            return None
    except Exception as e:
        logging.error("Ошибка Apollo метода: %s", e)
        return None

def get_followers_direct(html):
    """Прямой поиск в HTML"""
    try:
        followers_pattern = r'>(\d+)\s+Followers<'
        match = re.search(followers_pattern, html)
        if match:
            followers = int(match.group(1))
            logging.info("Прямой поиск: найдено подписчиков: %s", followers)
            return followers
        else:
            logging.warning("Прямой поиск не дал результата")
            return None
    except Exception as e:
        logging.error("Ошибка прямого поиска: %s", e)
        return None

def get_medium_followers():
    """
    Получает количество подписчиков для Medium пользователя @Eleron.
    Сначала пытается извлечь данные через Apollo State, если не удалось — выполняет прямой поиск.
    Возвращает число подписчиков или None, если данные получить не удалось.
    """
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        html_content = response.text
        followers = get_followers_apollo(html_content) or get_followers_direct(html_content)
        if followers is not None:
            logging.info("Общее количество подписчиков Medium: %s", followers)
        else:
            logging.warning("Данные о подписчиках Medium не найдены")
        return followers
    except Exception as e:
        logging.error("Общая ошибка при получении данных Medium: %s", e)
        return None

if __name__ == "__main__":
    followers = get_medium_followers()
    if followers is not None:
        print(f"Количество подписчиков: {followers}")
    else:
        print("Данные о подписчиках не найдены")
