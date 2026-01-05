from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения из переменных окружения."""
    
    # PostgreSQL настройки
    POSTGRES_USER: str = "ecommerce_user"
    POSTGRES_PASSWORD: str = "store_db_2024"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "ecommerce_db"
    
    # JWT настройки
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def database_url_async(self) -> str:
        """Возвращает строку подключения для асинхронного PostgreSQL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def database_url_sync(self) -> str:
        """Возвращает строку подключения для синхронного PostgreSQL."""
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


# Создаём экземпляр настроек
settings = Settings()

# Экспортируем для удобства использования в auth.py
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
