### HTTP команды для взаимодействия с API (порт 8090, IP 194.35.119.49)

#### 1. **Проверка статуса API**
- **Описание**: Проверить, работает ли сервер.
- **Метод**: `GET`
- **URL**: `/`
- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/"
  ```
- **Ответ**:
  ```json
  {
    "message": "LinkedIn Followers API is running"
  }
  ```

---

#### 2. **Проверка статуса аутентификации LinkedIn API**
- **Описание**: Проверить, успешно ли выполнена аутентификация в LinkedIn API.
- **Метод**: `GET`
- **URL**: `/auth-status`
- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/auth-status"
  ```
- **Ответ**:
  ```json
  {
    "status": "authenticated" // или "not_authenticated"
  }
  ```

---

#### 3. **Принудительное обновление данных о подписчиках**
- **Описание**: Выполнить немедленное обновление данных о подписчиках.
- **Метод**: `POST`
- **URL**: `/update-now`
- **Пример запроса**:
  ```bash
  curl -X POST "http://194.35.119.49:8090/update-now"
  ```
- **Ответ**:
  ```json
  {
    "status": "success",
    "message": "Followers data updated immediately."
  }
  ```

---

#### 4. **Получение последних данных о подписчиках**
- **Описание**: Получить последнюю запись данных о подписчиках для указанного профиля.
- **Метод**: `GET`
- **URL**: `/latest-data`
- **Параметры запроса**:
  - `profile_id` (опционально): ID профиля LinkedIn (по умолчанию используется `PUBLIC_PROFILE_ID` из `.env`).
- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/latest-data?profile_id=default_id"
  ```

  Или для конкретного профиля:
  ```bash
  curl "http://194.35.119.49:8090/latest-data?profile_id=gamsakhurdiya"
  ```

- **Ответ**:
  ```json
  {
    "profile_id": "gamsakhurdiya",
    "latest_data": {
      "followers_count": 11753,
      "timestamp": "2025-01-20 18:14:52"
    }
  }
  ```

---

#### 5. **Получение статистики за периоды**
- **Описание**: Вычислить изменения количества подписчиков за 24 часа, неделю и месяц.
- **Метод**: `GET`
- **URL**: `/statistics`
- **Параметры запроса**:
  - `profile_id` (опционально): ID профиля LinkedIn (по умолчанию используется `PUBLIC_PROFILE_ID` из `.env`).
- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/statistics?profile_id=default_id"
  ```

  Или для конкретного профиля:
  ```bash
  curl "http://194.35.119.49:8090/statistics?profile_id=gamsakhurdiya"
  ```

- **Ответ**:
  ```json
  {
    "profile_id": "gamsakhurdiya",
    "statistics": {
      "24h": 1.5,
      "week": 4.2,
      "month": 12.8
    }
  }
  ```

---

### Примечания
- **IP сервера:** `194.35.119.49`
- **Порт:** `8090`
- **PROFILE_ID:** Укажите `default_id` или замените на другой идентификатор профиля LinkedIn (`gamsakhurdiya`, например).