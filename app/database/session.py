import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, class_=AsyncSession)

Base = declarative_base()

Base.metadata.create_all(bind=engine)
