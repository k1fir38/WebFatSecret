from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
)
async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False
)


async def get_async_session():
    async with async_session_maker() as session:
        yield session

