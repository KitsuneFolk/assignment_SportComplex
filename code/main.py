from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # Вказуємо каталог для шаблонів


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})  # Рендеринг HTML шаблону


@app.post("/visitors/", response_model=schemas.Visitor)
def create_visitor(visitor: schemas.VisitorCreate, db: Session = Depends(get_db)):
    db_visitor = models.Visitor(**visitor.dict())  # Створення екземпляру моделі Visitor
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor


@app.get("/visitors/{visitor_id}", response_model=schemas.Visitor)
def read_visitor(visitor_id: int, db: Session = Depends(get_db)):
    db_visitor = db.query(models.Visitor).filter(models.Visitor.id == visitor_id).first()
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    return db_visitor


@app.get("/visitors/",
         response_model=List[schemas.Visitor])  # Fix: Змінено list[schemas.Visitor] на List[schemas.Visitor]
def read_visitors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    visitors = db.query(models.Visitor).offset(skip).limit(limit).all()
    return visitors


@app.get("/visitors/search/", response_model=schemas.VisitorSearchResults)
def search_visitors(
        first_name: Optional[str] = Query(None, title="First Name"),
        last_name: Optional[str] = Query(None, title="Last Name"),
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
):
    query = db.query(models.Visitor)

    if first_name:
        query = query.filter(
            models.Visitor.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Visitor.last_name.ilike(f"%{last_name}%"))

    results = query.offset(skip).limit(limit).all()
    return schemas.VisitorSearchResults(results=results)


@app.put("/visitors/{visitor_id}", response_model=schemas.Visitor)
def update_visitor(visitor_id: int, visitor: schemas.VisitorUpdate, db: Session = Depends(get_db)):
    db_visitor = db.query(models.Visitor).filter(models.Visitor.id == visitor_id).first()
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")

    for key, value in visitor.dict(exclude_unset=True).items():
        setattr(db_visitor, key, value)

    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor


@app.delete("/visitors/{visitor_id}", response_model=schemas.Visitor)
def delete_visitor(visitor_id: int, db: Session = Depends(get_db)):
    db_visitor = db.query(models.Visitor).filter(models.Visitor.id == visitor_id).first()
    if db_visitor is None:
        raise HTTPException(status_code=404, detail="Visitor not found")
    db.delete(db_visitor)
    db.commit()
    return db_visitor
