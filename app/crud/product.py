from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, insert, ScalarResult, func, text

from app.core.models.product import Product



async def find_all_product(session: AsyncSession) -> Sequence[Product]:

    query = (
        select(Product)
    )

    result = await session.execute(query)

    return result.scalars().all()

async def find_by_id_product(session: AsyncSession, product_id: int) -> Product | None:

    query = (
        select(Product)
        .where(Product.id == product_id)
    )

    result = await session.execute(query)
    return result.scalar_one_or_none()


async def find_by_name_product(
    session: AsyncSession,
    product_name: str,
    limit: int,
    offset: int
) -> Sequence[Product]:
    """
    query = (
        select(Product)
        .where(Product.name.ilike(f"%{product_name}%"))
        .limit(limit)   # применяем лимит
        .offset(offset) # применяем смещение
    )
    """
    # await session.execute(text("SET LOCAL pg_trgm.similarity_threshold = 0.2"))

    query = (
        select(Product)
        .where(Product.name.op('%')(product_name))  # Оператор схожести
        .order_by(func.similarity(Product.name, product_name).desc())  # Самые похожие — первыми
        .limit(limit)
    )
    result = await session.execute(query)
    return result.scalars().all()

