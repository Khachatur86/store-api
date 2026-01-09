from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    """
    Модель для создания отзыва
    """

    product_id: int = Field(..., description="ID товара, на который оставляется отзыв")
    comment: str | None = Field(
        None, max_length=1000, description="Текст отзыва (до 1000 символов)"
    )
    grade: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")

    model_config = ConfigDict(from_attributes=True)


class Review(BaseModel):
    """
    Модель для ответа с данными отзыва.
    """

    id: int = Field(..., description="Уникальный идентификатор отзыва")
    user_id: int = Field(..., description="ID пользователя, оставившего отзыв")
    product_id: int = Field(..., description="ID товара")
    comment: str | None = Field(None, description="Текст отзыва")
    comment_date: datetime = Field(..., description="Дата и время создания отзыва")
    grade: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    is_active: bool = Field(..., description="Активность отзыва")

    model_config = ConfigDict(from_attributes=True)
