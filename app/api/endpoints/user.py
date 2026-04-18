from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.schemas.user import UserRead, UserUpdate
from app.db.session import get_async_session
from app.crud.user import get_user_by_email, create_user, update_user
from app.core.security import PasswordHelper



router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/me", response_model=UserRead)
async def get_me(
        current_user = Depends(get_current_user),
):
    return current_user

@router.put("/me", response_model=UserRead)
async def update_me(
        user_in: UserUpdate,
        current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    update_data = user_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    user_update = await update_user(session=session, user=current_user)

    return user_update
