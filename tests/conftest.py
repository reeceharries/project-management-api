from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
import pytest

from app.db.dependencies import get_session
from app.db.test_engine import async_session_maker_test
from app.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        async with async_session_maker_test() as session:
            yield session
            await session.rollback()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
