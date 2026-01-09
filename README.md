# FastAPI Интернет-магазин

API для интернет-магазина на FastAPI с PostgreSQL.

## Требования

- Python 3.13+
- Docker и Docker Compose
- uv (для управления зависимостями)

## Установка

1. Установите зависимости:
```bash
uv sync
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Отредактируйте `.env` и укажите свои учетные данные для PostgreSQL

4. Запустите PostgreSQL в Docker:
```bash
docker-compose up -d
```

5. Примените миграции:
```bash
alembic upgrade head
```

## Запуск

```bash
uvicorn app.main:app --reload
```

API будет доступно по адресу: http://localhost:8000

## Документация

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Проверка типов

Проект использует [ty](https://github.com/astral-sh/ty) для статической проверки типов:

```bash
# Установка ty (если еще не установлен)
uv tool install ty

# Запуск проверки типов
uv tool run ty check app/models/ app/routers/ app/schemas/ --ignore unresolved-reference

# Или используйте удобный скрипт
./.ty-check.sh
```

**Примечание:** `--ignore unresolved-reference` используется для игнорирования forward references в SQLAlchemy моделях (это нормально для циклических зависимостей).

## Форматирование и линтинг

Проект использует [Ruff](https://github.com/astral-sh/ruff) для форматирования кода и линтинга:

```bash
# Проверка кода (без исправлений)
uv tool run ruff check app/

# Автоматическое исправление проблем
uv tool run ruff check --fix app/

# Форматирование кода
uv tool run ruff format app/

# Или используйте удобные скрипты
./.ruff-check.sh    # Проверка
./.ruff-fix.sh      # Исправление и форматирование
```

Ruff автоматически:
- Форматирует код в стиле Black
- Сортирует импорты (isort)
- Находит и исправляет проблемы с кодом
- Проверяет соответствие PEP 8

## Структура проекта

- `app/` - основной код приложения
  - `models/` - SQLAlchemy модели
  - `routers/` - FastAPI роутеры
  - `schemas/` - Pydantic схемы
  - `migrations/` - Alembic миграции
- `docker-compose.yml` - конфигурация PostgreSQL

## База данных

PostgreSQL запускается в Docker контейнере. Настройки подключения хранятся в файле `.env`:
- Пользователь: `POSTGRES_USER` (по умолчанию: `ecommerce_user`)
- Пароль: `POSTGRES_PASSWORD` (задайте в `.env`)
- База данных: `POSTGRES_DB` (по умолчанию: `ecommerce_db`)
- Хост: `POSTGRES_HOST` (по умолчанию: `localhost`)
- Порт: `POSTGRES_PORT` (по умолчанию: `5432`)

**Важно:** Файл `.env` не коммитится в git. Используйте `.env.example` как шаблон.
