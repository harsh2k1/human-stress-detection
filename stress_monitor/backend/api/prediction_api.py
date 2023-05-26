from fastapi import APIRouter
from pydantic import BaseModel

class RequestModel(BaseModel):
    userid: str
    password: str

prediction_api_router = APIRouter()
