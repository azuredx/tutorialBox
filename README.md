Учебный DevOps-проект: полноценное веб-приложение, полностью контейнеризированное с помощью Docker.

**Стек:** Python/Flask, PostgreSQL, Nginx, Docker, Docker Compose

## О проекте

Простое приложение для управления пользователями:
- Фронтенд на HTML/JavaScript (отдаётся через Nginx)
- REST API на Flask
- PostgreSQL для хранения данных
- Всё приложение запускается одной командой через Docker Compose

Проект создан для изучения основ DevOps: контейнеризация, работа с Docker Compose, управление окружением, миграции БД.

## Быстрый старт

### Требования
- Docker
- Docker Compose

### Запуск

```bash
# Клонировать репозиторий
git clone https://github.com/azuredx/tutorialBox
cd tutorialBox

# Запустить все сервисы
docker-compose up --build -d

# Инициализировать базу данных
docker-compose exec backend python init_db.py

# После запуска

-  Фронтенд: http://localhost
-  API: http://localhost:5000/users
-  ostgreSQL: localhost:5432

# Docker-образы

Проект состоит из трёх сервисов:

| Сервис     | Порты | Описание                     |
|------------|-------|------------------------------|
| `postgres` | 5432  | База данных PostgreSQL       |
| `backend`  | 5000  | Flask API с psycopg2         |
| `frontend` | 80    | Nginx с HTML/JS              |

# Переменные окружения

Конфигурация через переменные окружения (в `docker-compose.yml`):

```yaml
backend:
  environment:
    DB_HOST: postgres
    DB_NAME: mydb
    DB_USER: myuser
    DB_PASSWORD: mypassword

# Чему я научился

-  Ручной разворот приложения на голом Linux
-  Контейнеризация приложений с Docker
-  Оркестрация нескольких контейнеров с Docker Compose
-  Работа с PostgreSQL в Docker
-  Переменные окружения для конфигурации
-  Миграции и инициализация БД
-  Zero-downtime обновление (rolling update)

# Лицензия

Проект распространяется под лицензией MIT.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
MIT © [azure](https://github.com/azuredx) — см. файл [LICENSE](LICENSE)
---

#💻 Автор

**azure**  
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/azuredx)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/roo21k)
