from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import sys
sys.path.append("")
from backend.Kafka.producer import Producer
from backend.services.config_service import read_config
config = read_config()

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GetUser(BaseModel):
    username: str
    limit: str
    sensorFlag: bool

@app.post("/produceData")
async def start_capturing_data(form_data: GetUser):
    import glob
    import os
    if not form_data.sensorFlag:
        if form_data.limit == "all":
            for file in glob.glob(os.path.join('backend/'+config['TRAINING']['data.base.dir'], "*.csv")):
                Producer().produce_from_csv(filepath=file, key = form_data.username)
        else:
            for file in glob.glob(os.path.join(), "*.csv"):
                if file.split(os.path.sep)[-1].split(".csv")[0].replace("HR","") in range(1, int(form_data.limit)+1):
                    # Producer().produce_from_csv(filepath=file, key = form_data.username.encode('utf-8'))
                    Producer().produce_from_csv(filepath=file, key = 'test')
    else:
        Producer().produce_from_sensor()

if __name__ == "__main__":
    import sys
    port = sys.argv[1]
    uvicorn.run(app, port=int(port), host="0.0.0.0")
