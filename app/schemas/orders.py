from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.products import Product


class OrderItemSchema(BaseModel):
    id: int = Field(..., description="ID позиции товара")
    product_id: int = Field(..., description="ID товара")
    quantity: int = Field(..., description="Количество", ge=1)
    unit_price: Decimal = Field(..., description="Цена за единицу на момент покупки", ge=0)
    total_price: Decimal = Field(..., ge=0, description="Сумма по позиции")
    product: Product | None = Field(None, description="Полная информация о товаре")

    model_config = ConfigDict(from_attributes=True)


class OrderSchema(BaseModel):
    id: int = Field(..., description="ID заказа")
    user_id: int = Field(..., description="ID пользователя")
    status: str = Field(..., description="Текущий статус заказа")
    total_amount: Decimal = Field(..., ge=0, description="Общая стоимость")
    created_at: datetime = Field(..., description="Когда заказ был создан")
    updated_at: datetime = Field(..., description="Когда последний раз обновлялся")
    items: list[OrderItemSchema] = Field(default_factory=list, description="Список позиций")

    model_config = ConfigDict(from_attributes=True)


class OrderListSchema(BaseModel):
    items: list[OrderSchema] = Field(..., description="Заказы на текущей странице")
    total: int = Field(ge=0, description="Общее количество заказов")
    page: int = Field(ge=1, description="Текущая страница")
    page_size: int = Field(ge=1, description="Размер страницы")

    model_config = ConfigDict(from_attributes=True)
