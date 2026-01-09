from collections.abc import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.database import SessionLocal, async_session_maker


def get_db() -> Generator[Session]:
    """
    Зависимость для получения синхронной сессии базы данных.
    Создаёт новую сессию для каждого запроса и закрывает её после обработки.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession]:
    """
    Зависимость для получения асинхронной сессии базы данных.
    Создаёт новую сессию для каждого запроса и закрывает её после обработки.
    """
    async with async_session_maker() as session:
        yield session
