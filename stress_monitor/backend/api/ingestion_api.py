from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import sys
sys.path.append("")
from backend.Kafka.consumer import Consumer

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GetUserName(BaseModel):
    username: str

@app.post("/consumeData")
async def start_capturing_data(form_data: GetUserName):
    asyncio.create_task(Consumer().data_automation(key=form_data.username))

    import requests
    import json

    url = "http://localhost:8001/produceData"

    payload = json.dumps({
        "username": form_data.username,
        "limit": "all",
        "sensorFlag": False
    })
    headers = {
        'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=payload)
    

if __name__ == "__main__":
    import sys
    port = sys.argv[1]
    uvicorn.run(app, port=int(port), host="0.0.0.0")