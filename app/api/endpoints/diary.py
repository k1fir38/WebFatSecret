from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession


from app.api.dependencies import get_current_user
from app.schemas.diary import DiaryEntryCreate, DiaryEntryRead, DiaryEntryUpdate
from app.db.session import get_async_session
from app.crud.diary import (
    create_diary_entry,
    get_user_diary_for_date,
    find_dairy_by_id,
    delete_diary_entry,
    update_diary,
)




router = APIRouter(tags=["Diary"], prefix="/diary")

@router.get("/{date}", response_model=list[DiaryEntryRead])
async def get_diary(
        date: date,
        current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    diary = await get_user_diary_for_date(
        session=session,
        user_id= current_user.id,
        diary_date=date
    )

    return diary


@router.post("/", response_model=DiaryEntryCreate)
async def add_diary(
        diary_in: DiaryEntryCreate,
        current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    diary = await create_diary_entry(
        session=session,
        diary_in=diary_in,
        user_id=current_user.id
    )

    return diary

@router.delete("/{dairy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
        dairy_id: int,
        current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session),
):
    diary = await find_dairy_by_id(session=session, dairy_id=dairy_id)

    if diary is None:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    if current_user.id != diary.user_id:
        raise HTTPException(
            status_code=403,
            detail="Access to the requested resource is denied"
        )

    await delete_diary_entry(session=session, diary_obj=diary)

    return None

@router.put("/{dairy_id}", response_model=DiaryEntryRead)
async def update_dairy(
        dairy_id: int,
        diary_in: DiaryEntryUpdate,
        current_user = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):

    diary = await find_dairy_by_id(session=session, dairy_id=dairy_id)

    if diary is None:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    if current_user.id != diary.user_id:
        raise HTTPException(
            status_code=403,
            detail="Access to the requested resource is denied"
        )

    update_data = diary_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(diary, field, value)

    diary_update = await update_diary(session=session, diary=diary)

    return diary_update
