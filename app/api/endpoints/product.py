

from fastapi import APIRouter, HTTPException, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas.product import ProductRead
from app.db.session import get_async_session
from app.crud.product import find_all_product,find_by_name_product

router = APIRouter(tags=["product"], prefix="/product")

@router.get(path="/", response_model=list[ProductRead])
async def get_products(
        session: AsyncSession = Depends(get_async_session)
):
    products = await find_all_product(session=session)

    if products is None:
        raise HTTPException(
            status_code=404,
            detail="Products not found"
        )
    return products


@router.get("/search", response_model=list[ProductRead])
async def search_products(
        name: str,
        page: int = Query(1, ge=1),  # Номер страницы, по умолчанию 1
        size: int = Query(20, ge=1, le=100),  # Размер страницы, макс 100
        session: AsyncSession = Depends(get_async_session)
):
    # Вычисляем, сколько записей нужно пропустить
    # Если страница 1: (1-1) * 20 = 0 пропустить
    # Если страница 2: (2-1) * 20 = 20 пропустить
    offset = (page - 1) * size

    products = await find_by_name_product(
        session=session,
        product_name=name,
        limit=size,
        offset=offset,
    )

    if not products:
        raise HTTPException(status_code=404, detail="Products not found")

    return products


