from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from src.config import Config
from src.database.linkedin_db import add_linkedin_data, get_latest_linkedin_data, get_followers_over_period
from src.utils.logger import setup_logger


logger = setup_logger()

USERNAME = "eleron96@gmail.com"
PASSWORD = "!Iamluckyman20"

def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def linkedin_login(driver, username, password):
    login_url = 'https://www.linkedin.com/login'
    logger.info(f"Переход на страницу логина: {login_url}")
    driver.get(login_url)
    try:
        wait = WebDriverWait(driver, 20)
        email_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = driver.find_element(By.ID, 'password')
        email_field.send_keys(username)
        password_field.send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        wait.until(EC.presence_of_element_located((By.ID, 'global-nav-search')))
        logger.info("Авторизация прошла успешно")
        return True
    except Exception as e:
        logger.error(f"Ошибка авторизации: {e}")
        return False

def fetch_followers(driver, profile_url):
    logger.info(f"Переход на страницу профиля: {profile_url}")
    driver.get(profile_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    followers_text = soup.find('span', class_='t-bold')
    if followers_text:
        followers = followers_text.get_text(strip=True)
        logger.info(f"Найдено количество подписчиков: {followers}")
        return followers
    logger.warning("Не удалось найти количество подписчиков")
    return None

def get_linkedin_followers():
    driver = setup_driver()
    try:
        if linkedin_login(driver, USERNAME, PASSWORD):
            profile_url = f'https://www.linkedin.com/in/{Config.LINKEDIN_PROFILE_ID}/'
            return fetch_followers(driver, profile_url)
    finally:
        driver.quit()
    return None

def fetch_and_store_linkedin_data():
    followers_count = get_linkedin_followers()
    if followers_count:
        add_linkedin_data(Config.LINKEDIN_PROFILE_ID, followers_count)
        logger.info(f"LinkedIn данные обновлены: {followers_count}")
    else:
        logger.warning("Не удалось получить данные LinkedIn.")

def get_latest_linkedin(profile_id=None):
    if profile_id is None:
        profile_id = Config.LINKEDIN_PROFILE_ID
    return get_latest_linkedin_data(profile_id)

def get_linkedin_statistics(profile_id):
    periods = {
        "24h": datetime.now() - timedelta(hours=24),
        "week": datetime.now() - timedelta(weeks=1),
        "month": datetime.now() - timedelta(days=30)
    }
    stats = {}
    for period, start_time in periods.items():
        trend = get_followers_over_period(profile_id, start_time)
        stats[period] = trend
    return stats