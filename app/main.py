from fastapi import FastAPI, Depends, HTTPException
from app.database.session import SessionLocal
from app.schemas.email import EmailCreate, Email
from app.models.email import Email as EmailModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/email", response_model=Email)
async def create_email(email: EmailCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailModel).where(EmailModel.email == email.email))
    db_email = result.scalars().first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_email = EmailModel(email=email.email)
    db.add(db_email)
    await db.commit()
    await db.refresh(db_email)
    return db_email


@app.get("/email", response_model=List[Email])
async def read_emails(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EmailModel).offset(skip).limit(limit))
    emails = result.scalars().all()
    return emails
