from fastapi import APIRouter
import uvicorn
from pydantic import BaseModel

import sys
sys.path.append("")
from core.service.process_data_service import data_automation

class ReqModel(BaseModel):
    userid: str
    password: str

prediction_api_router = APIRouter()

@prediction_api_router.post('/processData')
def process(request_body:ReqModel):
    data_automation(key=request_body.userid)
