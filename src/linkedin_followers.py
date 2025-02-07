import time
import random
import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Чтобы автоматически подбирать совместимый ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

USERNAME = "eleron96@gmail.com"
PASSWORD = "!Iamluckyman20"

def setup_driver(headless=True):
    logging.info("Настройка драйвера с помощью webdriver_manager")
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")  # <--- ВАЖНО!!!
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    logging.info("Драйвер запущен")
    return driver



def type_with_delay(element, text, min_delay=0.1, max_delay=0.3):
    """Имитация набора текста с небольшими задержками между символами."""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

def linkedin_login(driver, username, password):
    login_url = 'https://www.linkedin.com/login'
    logging.info(f"Переход на страницу логина: {login_url}")
    driver.get(login_url)

    try:
        wait = WebDriverWait(driver, 20)
        email_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = driver.find_element(By.ID, 'password')

        logging.info("Ввод логина")
        type_with_delay(email_field, username)
        time.sleep(random.uniform(0.5, 1.0))

        logging.info("Ввод пароля")
        type_with_delay(password_field, password)

        sign_in_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        logging.info("Нажатие на кнопку входа")
        sign_in_button.click()

        # Ожидаем появления элемента, характерного для авторизованной страницы
        wait.until(EC.presence_of_element_located((By.ID, 'global-nav-search')))
        logging.info("Авторизация прошла успешно")
        time.sleep(random.uniform(2, 4))
        return True

    except Exception as e:
        logging.error(f"Ошибка авторизации: {e}")
        return False

def fetch_followers(driver, profile_url):
    logging.info(f"Переход на страницу профиля: {profile_url}")
    driver.get(profile_url)

    try:
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except Exception as e:
        logging.error(f"Ошибка ожидания загрузки страницы: {e}")
        return None

    time.sleep(random.uniform(3, 6))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Ищем ссылку с упоминанием "подписчик" или "followers"
    followers_link = None
    for a in soup.find_all('a'):
        if a.text and ("подписчик" in a.text.lower() or "followers" in a.text.lower()):
            followers_link = a
            break

    if followers_link:
        bold_span = followers_link.find('span', class_='t-bold')
        if bold_span:
            followers = bold_span.get_text(strip=True)
            logging.info(f"Найдено количество подписчиков: {followers}")
            return followers
        else:
            match = re.search(r'(\d[\d\s,.]*)', followers_link.get_text())
            if match:
                followers = match.group(1).strip()
                logging.info(f"Найдено количество подписчиков: {followers}")
                return followers

    logging.warning("Элемент с информацией о подписчиках не найден")
    return None

def get_followers_count(profile_url, headless=True):
    """
    Запускает драйвер, авторизуется и возвращает количество подписчиков.
    Использует webdriver_manager для автоматического подбора chromedriver.
    """
    driver = setup_driver(headless)
    try:
        if not linkedin_login(driver, USERNAME, PASSWORD):
            logging.error("Не удалось авторизоваться в LinkedIn")
            return None
        return fetch_followers(driver, profile_url)
    finally:
        logging.info("Закрытие драйвера")
        driver.quit()

if __name__ == "__main__":
    # Тестовый запуск
    profile_url = "https://www.linkedin.com/in/gamsakhurdiya/"
    count = get_followers_count(profile_url, headless=True)
    if count:
        logging.info(f"Количество подписчиков: {count}")
    else:
        logging.info("Информация о подписчиках недоступна")
