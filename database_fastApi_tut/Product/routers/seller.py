from fastapi import APIRouter, status, Response
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models
from typing import List
from ..import schemas as sh
from passlib.context import CryptContext


router  = APIRouter(
    tags=['Seller'],
    prefix='/seller'
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=sh.DisplaySeller)
def create_seller(request: sh.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(username = request.username, email = request.email, password = hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return new_seller

@router.get("/", response_model=List[sh.DisplaySeller])
def products(db: Session = Depends(get_db)):
    sellers = db.query(models.Seller).all()
    return sellers