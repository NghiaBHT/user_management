import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

import pytest_asyncio
from httpx import AsyncClient
from fastapi import FastAPI

from app.main import create_app 

@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    import asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function") 
async def app() -> FastAPI:
    return create_app()

@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac 