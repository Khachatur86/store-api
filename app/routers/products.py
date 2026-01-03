from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.db_depends import get_db

# Создаём маршрутизатор для товаров
router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    """
    Возвращает список всех товаров.
    """
    stmt = select(ProductModel).where(ProductModel.is_active == True)
    result = await db.execute(stmt)
    products = result.scalars().all()
    return products


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Создаёт новый товар.
    """
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == product.category_id,
        CategoryModel.is_active == True
    )
    category_result = await db.execute(category_stmt)
    category = category_result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Category not found or inactive")

    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product



@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """
    Возвращает список товаров в указанной категории по её ID.
    """
    category_stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True)
    category_result = await db.execute(category_stmt)
    category = category_result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Category not found or inactive")

    products_stmt = select(ProductModel).where(
        ProductModel.category_id == category_id,
        ProductModel.is_active == True
    )
    products_result = await db.execute(products_stmt)
    products = products_result.scalars().all()
    return products


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Возвращает детальную информацию о товаре по его ID.
    """
    stmt = select(ProductModel).where(
        ProductModel.id == product_id,
        ProductModel.is_active == True
    )
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    """
    Обновляет товар по его ID.
    """
    stmt = select(ProductModel).where(
        ProductModel.id == product_id,
        ProductModel.is_active == True
    )
    result = await db.execute(stmt)
    db_product = result.scalar_one_or_none()

    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Проверка существования категории, если category_id изменяется
    if product.category_id != db_product.category_id:
        category_stmt = select(CategoryModel).where(
            CategoryModel.id == product.category_id,
            CategoryModel.is_active == True
        )
        category_result = await db.execute(category_stmt)
        category = category_result.scalar_one_or_none()

        if not category:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Category not found or inactive")

    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(**product.model_dump())
    )
    await db.commit()
    await db.refresh(db_product)
    return db_product


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """
    Удаляет товар по его ID.
    """
    stmt = select(ProductModel).where(
        ProductModel.id == product_id,
        ProductModel.is_active == True
    )
    result = await db.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found or inactive")

    product.is_active = False
    await db.commit()
    return {"status": "success", "message": "Product marked as inactive"}
