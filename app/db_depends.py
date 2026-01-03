from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from collections.abc import AsyncGenerator

from app.database import async_session_maker


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения асинхронной сессии базы данных.
    Создаёт новую сессию для каждого запроса и закрывает её после обработки.
    """
    async with async_session_maker() as session:
        yield session
