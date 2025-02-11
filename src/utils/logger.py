import logging
import sys

def setup_logger(name="followers_logger", level=logging.INFO):
    """Настройка логгера для проекта."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Создание логгера
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Потоковый хендлер (консоль)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Убираем дублирование логов при многократном вызове setup_logger
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
