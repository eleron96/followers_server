### **HTTP команды для взаимодействия с API (порт 8090, IP 194.35.119.49)**

---

#### **1. Проверка статуса API**
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
    "message": "Followers API is running"
  }
  ```

---

#### **2. Принудительное обновление данных о подписчиках**

##### **LinkedIn**
- **Метод**: `POST`
- **URL**: `/linkedin-update`
- **Пример запроса**:
  ```bash
  curl -X POST "http://194.35.119.49:8090/linkedin-update"
  ```
- **Ответ**:
  ```json
  {
    "status": "success",
    "latest": {
      "count": "11,865",
      "timestamp": "2025-02-10 16:56:09"
    }
  }
  ```

##### **YouTube**
- **Метод**: `POST`
- **URL**: `/youtube-update`
- **Пример запроса**:
  ```bash
  curl -X POST "http://194.35.119.49:8090/youtube-update"
  ```
- **Ответ**:
  ```json
  {
    "status": "success",
    "latest": {
      "count": 57100,
      "timestamp": "2025-02-10 16:55:45"
    }
  }
  ```

##### **Medium**
- **Метод**: `POST`
- **URL**: `/medium-update`
- **Пример запроса**:
  ```bash
  curl -X POST "http://194.35.119.49:8090/medium-update"
  ```
- **Ответ**:
  ```json
  {
    "status": "success",
    "latest": {
      "count": 189,
      "timestamp": "2025-02-10 16:55:46"
    }
  }
  ```

---

#### **3. Получение последних данных о подписчиках**

##### **LinkedIn**
- **Метод**: `GET`
- **URL**: `/linkedin-latest`
- **Параметры запроса**:
  - `profile_id` (опционально): ID профиля LinkedIn (по умолчанию используется `PUBLIC_PROFILE_ID` из `.env`).
  
- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/linkedin-latest?profile_id=gamsakhurdiya"
  ```

- **Ответ**:
  ```json
  {
    "platform": "linkedin",
    "profile_id": "gamsakhurdiya",
    "latest_data": {
      "count": "11,865",
      "timestamp": "2025-02-10 16:56:09"
    }
  }
  ```

---

##### **YouTube**
- **Метод**: `GET`
- **URL**: `/youtube-latest`
  
- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/youtube-latest"
  ```

- **Ответ**:
  ```json
  {
    "platform": "youtube",
    "latest_data": {
      "count": 57100,
      "timestamp": "2025-02-10 16:55:45"
    }
  }
  ```

---

##### **Medium**
- **Метод**: `GET`
- **URL**: `/medium-latest`

- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/medium-latest"
  ```

- **Ответ**:
  ```json
  {
    "platform": "medium",
    "latest_data": {
      "count": 189,
      "timestamp": "2025-02-10 16:55:46"
    }
  }
  ```

---

#### **4. Получение статистики за периоды**

##### **LinkedIn**
- **Метод**: `GET`
- **URL**: `/statistics`
- **Параметры запроса**:
  - `profile_id` (опционально): ID профиля LinkedIn (по умолчанию используется `PUBLIC_PROFILE_ID` из `.env`).

- **Пример запроса**:
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

##### **YouTube**
- **Метод**: `GET`
- **URL**: `/youtube-statistics`
- **Параметры запроса**:
  - `channel_id` (опционально): ID YouTube-канала (по умолчанию используется `YOUTUBE_CHANNEL_ID` из `.env`).

- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/youtube-statistics?channel_id=UCRhID0powzDpE4D2KuVKGHg"
  ```

- **Ответ**:
  ```json
  {
    "channel_id": "UCRhID0powzDpE4D2KuVKGHg",
    "statistics": {
      "24h": 0.18,
      "week": 0.18,
      "month": 0.18
    }
  }
  ```

---

##### **Medium**
- **Метод**: `GET`
- **URL**: `/medium-statistics`
- **Параметры запроса**:
  - `username` (опционально): Имя пользователя Medium (по умолчанию используется `MEDIUM_USERNAME` из `.env`).

- **Пример запроса**:
  ```bash
  curl "http://194.35.119.49:8090/medium-statistics?username=Eleron"
  ```

- **Ответ**:
  ```json
  {
    "username": "Eleron",
    "statistics": {
      "24h": 0.0,
      "week": 1.07,
      "month": 1.07
    }
  }
  ```

---

### **Примечания**
- **IP сервера:** `194.35.119.49`
- **Порт:** `8090`
- **PROFILE_ID (LinkedIn):** Укажите `default_id` или замените на другой идентификатор профиля LinkedIn (`gamsakhurdiya`, например).
- **CHANNEL_ID (YouTube):** По умолчанию используется `UCRhID0powzDpE4D2KuVKGHg`, но вы можете указать другой.
- **USERNAME (Medium):** По умолчанию используется `Eleron`, но вы можете указать другого пользователя.

---
