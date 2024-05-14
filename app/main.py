from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import SessionLocal
from schemas.email import EmailCreate, Email
from models.email import Email as EmailModel
from typing import List

app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/email", response_model=Email)
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    db_email = db.query(EmailModel).filter(
        EmailModel.email == email.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_email = EmailModel(email=email.email)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email


@app.get("/email", response_model=List[Email])
def read_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emails = db.query(EmailModel).offset(skip).limit(limit).all()
    return emails
