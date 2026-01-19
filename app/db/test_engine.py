from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core.config import get_settings

settings = get_settings()

test_engine = create_async_engine(
    str(settings.database_url_test),
    future=True,
)

async_session_maker_test = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)
