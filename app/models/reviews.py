# Создайте модель Review в app/models/reviews.py с использованием SQLAlchemy. Поля модели:
#
# id: Числовое поле, первичный ключ, автоинкремент.
# user_id: Внешний ключ, связывающий отзыв с таблицей users (модель User).
# product_id: Внешний ключ, связывающий отзыв с таблицей products (модель Product).
# comment: Текстовое поле для отзыва, необязательное (может быть пустым).
# comment_date: Поле даты и времени, автоматически заполняется текущей датой (default=datetime.now).
# grade: Числовое поле (оценка от 1 до 5), обязательное.
# is_active: Булево поле, по умолчанию True (для мягкого удаления).
from app.database import Base
from datetime import datetime
from sqlalchemy import ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ReviewModel(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    grade: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="reviews")
    product: Mapped["ProductModel"] = relationship("ProductModel", back_populates="reviews")