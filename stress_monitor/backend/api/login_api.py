from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append("")
from backend.services.identifier_generation import generate_hash_uid, verify_password

class CreateUser(BaseModel):
    username: str
    password: str
    email: str

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Initialize the database
engine = create_engine("sqlite:///./users.db", echo=True)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
login_api_router = APIRouter()

@login_api_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    print(username, password)
    # For demonstration purposes, assume authentication is successful and return a dummy token
    token = "dummy_token"

    session = SessionLocal()
    
    if not session.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    hashed_password = session.query(User).filter(User.username == username).first().hashed_password
    if not verify_password(password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # If authentication is successful, return the JWT token
    return {"access_token": token, "token_type": "bearer", "userId": username}


@login_api_router.post("/createUser")
async def create_new_user(user: CreateUser):

    session = SessionLocal()

    if session.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if session.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = generate_hash_uid(user.password)
    

    # Create a new user
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    
    # Return a success message
    return {"message": "User registered successfully"}


@login_api_router.get("/allUsers")
async def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    return [user.__dict__ for user in users]


@login_api_router.get("/")
async def home():
    return {"ping":"pong"}
