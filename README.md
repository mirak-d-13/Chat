# Chat

Добро пожаловать в тестовое задание по созданию real-time чата на FastAPI.

## Стек технологий

- **FastAPI** — современный веб-фреймворк
- **PostgreSQL** — реляционная база данных
- **SQLAlchemy 2.0** — ORM с поддержкой async
- **Alembic** — миграции базы данных
- **Docker & Docker Compose** — контейнеризация
- **JWT** — авторизация
- **WebSockets** — для real-time чата

---

## Быстрый старт

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/mirak-d-13/Chat.git
cd Chat
```

---

2. **Создайте файл .env**

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=chatdb
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/chatdb

JWT_SECRET_KEY=supersecret
```

---

3.	**Запустите проект**
```bash
docker-compose build --no-cache
docker-compose up
```

---

4. Создайте миграции
```bash
docker-compose exec web alembic revision --autogenerate -m "Initial migration"
```

---

5. Примените миграцию
```bash
docker-compose exec web alembic upgrade head
```

---

6. Сгенерируйте пользователей для тестирования
```bash
docker-compose exec web python -m app.create_test_data
```
---

7. После запуска перейдите
```angular2html
http://0.0.0.0:8000/docs
```

---
```python
Chat/
│
├── app/                       # Основная директория с приложением FastAPI
│   ├── api/                   # Папка с роутерами
│   ├── core/                  # Конфигурации, аутентификация  
│   ├── db/                    # База данных (модели, репозитории)
│   ├── schemas/               # Pydantic схемы
│   ├── websockets/            # Реализация WebSocket
│   └── create_test_data.py    # Скрипт для генерации тестовых данных
│
├── alembic/                   # Миграции базы данных
├── alembic.ini                # Конфигурация для Alembic
├── docker-compose.yml         # Docker Compose файл
├── Dockerfile                 # Dockerfile для сборки контейнера
├── .env                       # Переменные окружения (создайте)
├── requirements.txt           # Зависимости Python
└── README.md                  # Документация проекта
```