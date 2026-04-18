from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, insert, ScalarResult


from app.schemas.user import UserCreate
from app.core.security import PasswordHelper
from app.core.models.user import User



async def create_user(session: AsyncSession, user_in: UserCreate) -> User:

    hashed_password = PasswordHelper.hash_password(password=user_in.password)

    db_user = User(
        username=user_in.username,
        name=user_in.name,
        email=user_in.email,
        hashed_password=hashed_password,
        gender=user_in.gender,
        birth_date=user_in.birth_date,
        weight=user_in.weight,
        height=user_in.height,
        activity_level=user_in.activity_level,
        goal=user_in.goal
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

async def get_user_by_email(session: AsyncSession, email: str) -> User | None:

    query = select(User).where(User.email == email)
    result = await session.execute(query)

    return result.scalar_one_or_none()

async def get_user_by_id(session: AsyncSession, id: int) -> User | None:

    query = select(User).where(User.id == id)
    result = await session.execute(query)

    return result.scalar_one_or_none()

async def update_user(session: AsyncSession, user) -> User | None:
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user