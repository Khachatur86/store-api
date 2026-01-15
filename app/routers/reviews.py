from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import get_current_buyer, get_current_user
from app.db_depends import get_async_db
from app.models import ProductModel, UserModel
from app.models.reviews import ReviewModel
from app.schemas import ReviewCreateSchema, ReviewSchema

router = APIRouter(prefix="/reviews", tags=["Reviews"])


async def update_product_rating(db: AsyncSession, product_id: int):
    """
    Пересчитывает средний рейтинг товара на основе всех активных отзывов.
    Обновляет поле rating в модели Product без commit.
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id, ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0

    product = await db.get(ProductModel, product_id)
    if product:
        product.rating = float(avg_rating)


@router.get("/", response_model=list[ReviewSchema])
async def get_reviews(db: Annotated[AsyncSession, Depends(get_async_db)]):
    """
    Возвращает список всех активных отзывов
    """
    reviews_stmt = select(ReviewModel).where(ReviewModel.is_active.is_(True))
    return (await db.scalars(reviews_stmt)).all()


@router.post("/", response_model=ReviewSchema)
async def create_review(
    review_payload: ReviewCreateSchema,
    db: Annotated[AsyncSession, Depends(get_async_db)],
    buyer: Annotated[UserModel, Depends(get_current_buyer)],
):
    """
    Создает отзыв
    :param review_payload: тело запроса отзыва
    :param db: сесиия базы данных
    :param buyer:
    :return:
    """
    product = await db.get(ProductModel, review_payload.product_id)

    if not product or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {review_payload.product_id} is not found",
        )
    db_review = ReviewModel(**review_payload.model_dump(), user_id=buyer.id)
    db.add(db_review)
    await db.flush()

    await update_product_rating(db, review_payload.product_id)

    await db.commit()
    await db.refresh(db_review)

    return db_review


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    db: Annotated[AsyncSession, Depends(get_async_db)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """
    Мягкое удаление отзыва по review_id.
    Доступ: Автор отзыва или пользователи с ролью "admin".
    После удаления пересчитывает рейтинг товара.
    """
    review: ReviewModel | None = await db.get(ReviewModel, review_id)

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if not review.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review is already inactive"
        )

    is_author = review.user_id == current_user.id
    is_admin = current_user.role == "admin"

    if not (is_author or is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this review",
        )

    product_id: int = int(review.product_id)

    review.is_active = False

    await db.flush()

    await update_product_rating(db, product_id)

    await db.commit()

    return {"message": "Review deleted"}
