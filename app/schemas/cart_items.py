from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.products import ProductSchema


class CartItemBaseSchema(BaseModel):
    product_id: int = Field(description="ID товара")
    quantity: int = Field(ge=1, description="Количество товара")


class CartItemCreateSchema(CartItemBaseSchema):
    """Модель для добавления нового товара в корзину."""

    pass


class CartItemUpdateSchema(BaseModel):
    """Модель для обновления количества товара в корзине."""

    quantity: int = Field(..., ge=1, description="Новое количество товара")


class CartItemSchema(BaseModel):
    """Товар в корзине с данными продукта."""

    id: int = Field(..., description="ID позиции корзины")
    quantity: int = Field(..., ge=1, description="Количество товара")
    product: ProductSchema = Field(..., description="Информация о товаре")

    model_config = ConfigDict(from_attributes=True)


class CartSchema(BaseModel):
    """Полная информация о корзине пользователя."""

    user_id: int = Field(..., description="ID пользователя")
    items: list[CartItemSchema] = Field(default_factory=list, description="Содержимое корзины")
    total_quantity: int = Field(..., ge=0, description="Общее количество товаров")
    total_price: Decimal = Field(..., ge=0, description="Общая стоимость товаров")

    model_config = ConfigDict(from_attributes=True)
