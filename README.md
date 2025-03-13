
---

### **HTTP команды для взаимодействия с API (порт 8090, IP 194.35.119.49)**

---

#### **1. Проверка статуса API**
Проверка работы сервера.

```bash
curl "http://194.35.119.49:8090/"
```

---

#### **2. Принудительное обновление данных о подписчиках**

**LinkedIn**
```bash
curl -X POST "http://194.35.119.49:8090/linkedin/update"
```

**YouTube**
```bash
curl -X POST "http://194.35.119.49:8090/youtube/update"
```

**Medium**
```bash
curl -X POST "http://194.35.119.49:8090/medium/update"
```

**Instagram**
```bash
curl -X POST "http://194.35.119.49:8090/instagram/update"
```

---

#### **3. Получение последних данных о подписчиках**

**LinkedIn**
```bash
curl "http://194.35.119.49:8090/linkedin/latest?profile_id=gamsakhurdiya"
```

**YouTube**
```bash
curl "http://194.35.119.49:8090/youtube/latest?channel_id=UCRhID0powzDpE4D2KuVKGHg"
```

**Medium**
```bash
curl "http://194.35.119.49:8090/medium/latest?username=Eleron"
```

**Instagram**
```bash
curl "http://194.35.119.49:8090/instagram/latest?username=nikog_bim"
```

---

#### **4. Получение статистики за периоды (24 часа, неделя, месяц)**

**LinkedIn**
```bash
curl "http://194.35.119.49:8090/linkedin/statistics?profile_id=gamsakhurdiya"
```

**YouTube**
```bash
curl "http://194.35.119.49:8090/youtube/statistics?channel_id=UCRhID0powzDpE4D2KuVKGHg"
```

**Medium**
```bash
curl "http://194.35.119.49:8090/medium/statistics?username=Eleron"
```

**Instagram**
```bash
curl "http://194.35.119.49:8090/instagram/statistics?username=nikog_bim"
```

---

#### **5. Получение ежедневной статистики за последние 30 дней**

Эти данные можно использовать для построения графиков.

**LinkedIn**
```bash
curl "http://194.35.119.49:8090/linkedin/daily-stats?profile_id=gamsakhurdiya"
```

**YouTube**
```bash
curl "http://194.35.119.49:8090/youtube/daily-stats?channel_id=UCRhID0powzDpE4D2KuVKGHg"
```

**Medium**
```bash
curl "http://194.35.119.49:8090/medium/daily-stats?username=Eleron"
```

**Instagram**
```bash
curl "http://194.35.119.49:8090/instagram/daily-stats?username=nikog_bim"
```

---

### **Примеры ответов**

#### **Последние данные о подписчиках (LinkedIn)**

```json
{
  "platform": "linkedin",
  "profile_id": "gamsakhurdiya",
  "latest_data": {
    "followers_count": 11752,
    "timestamp": "2025-01-20 18:14:52"
  }
}
```

#### **Статистика за периоды (YouTube)**

```json
{
  "channel_id": "UCRhID0powzDpE4D2KuVKGHg",
  "statistics": {
    "24h": 1.5,
    "week": 4.2,
    "month": 12.8
  }
}
```

#### **Ежедневная статистика (Medium)**

```json
{
  "username": "Eleron",
  "daily_stats": [
    {"date": "2025-01-20", "followers_count": 2500},
    {"date": "2025-01-21", "followers_count": 2515},
    {"date": "2025-01-22", "followers_count": 2530},
    "..."
  ]
}
```

#### **Последние данные о подписчиках (Instagram)**

```json
{
  "platform": "instagram",
  "latest_data": {
    "count": 1234,
    "timestamp": "2024-03-13 10:00:00"
  }
}
```

#### **Статистика за периоды (Instagram)**

```json
{
  "username": "nikog_bim",
  "statistics": {
    "24h": 2.5,
    "week": 5.8,
    "month": 15.3
  }
}
```

#### **Ежедневная статистика (Instagram)**

```json
{
  "username": "nikog_bim",
  "daily_stats": [
    {"date": "2024-02-13", "followers_count": 1200},
    {"date": "2024-02-14", "followers_count": 1215},
    {"date": "2024-02-15", "followers_count": 1230},
    "..."
  ]
}
```

---

### **Примечания**

- **IP сервера:** `194.35.119.49`
- **Порт:** `8090`
- **Параметры запроса:**
  - `profile_id` для LinkedIn
  - `channel_id` для YouTube
  - `username` для Medium и Instagram
