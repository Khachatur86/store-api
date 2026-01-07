from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth import get_current_buyer
from app.db_depends import get_async_db
from app.models import Product as ProductModel, User as UserModel
from app.schemas import Review, ReviewCreate
from app.models.reviews import Review as ReviewModel
router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

async def update_product_rating(db: AsyncSession, product_id: int):
    """
    Пересчитывает средний рейтинг товара на основе всех активных отзывов.
    Обновляет поле rating в модели Product без commit.
    """
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0

    product = await db.get(ProductModel, product_id)
    if product:
        product.rating = float(avg_rating)


@router.get("/", response_model=list[Review])
async def get_reviews(db: Annotated[AsyncSession, Depends(get_async_db)]):
    """
    Возвращает список всех активных отзывов
    """
    reviews_stmt = select(
        ReviewModel
    ).where(
        ReviewModel.is_active.is_(True)
    )
    return (await db.scalars(reviews_stmt)).all()


@router.post("/", response_model=Review)
async def create_review(
        review_payload: ReviewCreate,
        db: Annotated[AsyncSession, Depends(get_async_db)],
        buyer: Annotated[UserModel, Depends(get_current_buyer)]
):
    product = await db.get(ProductModel, review_payload.product_id)

    if not product or not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {review_payload.product_id} is not found"
        )
    db_review = ReviewModel(**review_payload.model_dump(), user_id=buyer.id)
    db.add(db_review)
    await db.flush()

    await update_product_rating(db, review_payload.product_id)
    
    await db.commit()
    await db.refresh(db_review)
    
    return db_review





@router.delete("/{review_id}")
async def delete_review():
    ...
