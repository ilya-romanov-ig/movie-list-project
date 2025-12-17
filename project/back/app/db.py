from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# 👉 Добавляем алиас, чтобы security.jwt мог импортировать async_session
async_session = AsyncSessionLocal

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
