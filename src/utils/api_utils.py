import time
from functools import wraps
from src.utils.logger import setup_logger

logger = setup_logger()

def rate_limit(calls_per_hour=30):
    """
    Декоратор для ограничения частоты вызовов API
    """
    def decorator(func):
        last_reset = time.time()
        calls = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_reset, calls
            current_time = time.time()

            # Сброс счетчика каждый час
            if current_time - last_reset > 3600:
                calls = 0
                last_reset = current_time

            # Проверка лимита
            if calls >= calls_per_hour:
                wait_time = 3600 - (current_time - last_reset)
                logger.warning(f"Достигнут лимит вызовов API. Ожидание {wait_time:.2f} секунд")
                time.sleep(wait_time)
                calls = 0
                last_reset = time.time()

            calls += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

def retry_on_failure(max_retries=3, delay=5):
    """
    Декоратор для повторных попыток при сбоях
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Все попытки выполнить {func.__name__} не удались: {str(e)}")
                        raise
                    logger.warning(f"Попытка {attempt + 1} из {max_retries} не удалась: {str(e)}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator 