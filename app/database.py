from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Строка подключения для SQLite
DATABASE_URL_SQLITE = "sqlite:///ecommerce.db"

# Создаём Engine для SQLite
engine = create_engine(DATABASE_URL_SQLITE, echo=True)

# Настраиваем фабрику сеансов для SQLite
SessionLocal = sessionmaker(bind=engine)


# --------------- Асинхронное подключение к PostgreSQL -------------------------

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Строка подключения для PostgreSQL (из переменных окружения)
DATABASE_URL = settings.database_url_async

# Создаём асинхронный Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику асинхронных сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass
