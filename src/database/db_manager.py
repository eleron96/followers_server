import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ensure_db_exists(db_path, table_creation_query):
    """Проверяет существование базы данных и создает таблицу, если файл отсутствует."""
    if not os.path.exists(db_path):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(table_creation_query)
            conn.commit()
        logging.info(f"Создана новая база данных: {db_path}")

def insert_data(db_path, insert_query, data):
    """Вставляет данные в указанную таблицу базы данных."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(insert_query, data)
        conn.commit()

def fetch_latest_data(db_path, select_query, identifier):
    """Извлекает последние данные из базы по идентификатору."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(select_query, (identifier,))
        result = cursor.fetchone()
        return {"count": result[0], "timestamp": result[1]} if result else None
