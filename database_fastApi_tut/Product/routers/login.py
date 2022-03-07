from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..import  models, database, schemas as sh
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..database import get_db 
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schemas import TokenData

SECRET_KEY = "4d2bcaebc2ef9f19b9758f70a6683f08e86e9f8b4706a497a9d7a2c6a4aa7f2b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 20

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_toke(data: dict):
    to_encode = data.copy()
    expire  = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Seller).filter(
        models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Username not found."
    )
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Username not found."
    )

    access_token = generate_toke(data={
        "sub": user.username
    })

    return {"access_token":access_token, "token_type":"bearer "}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_execption = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_execption
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_execption
