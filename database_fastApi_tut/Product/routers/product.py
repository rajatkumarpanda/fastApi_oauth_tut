from fastapi import APIRouter, status, Response
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models
from typing import List
from ..import schemas as sh



router  = APIRouter(
    tags=['Product'],
    prefix='/product'
)

@router.delete("/{id}")
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session = False)
    db.commit()
    return {"Product deleted"}

@router.put("/{id}")
def update(id, request: sh.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    else:
        product.update(request.dict())

    db.commit()
    return {"Product Updated."}
    
@router.get("/", response_model=List[sh.DisplayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get("/{id}")
def product(id, response: Response,db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Product not found."}
    return product


@router.post("/", status_code = status.HTTP_201_CREATED)
def add(request: sh.Product, db: Session = Depends(get_db)):
    new_product = models.Product(name= request.name, 
    description = request.description, price= request.price, seller_id=1)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return request