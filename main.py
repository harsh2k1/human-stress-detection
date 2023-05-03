from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from core.service import config_service as cf
from api.heartrate_detection_api import prediction_api_router
from api.login_api import login_api_router

import sys
sys.path.append("")
from core.utilities.main_utils import *

app = FastAPI()
app.include_router(prediction_api_router)
app.include_router(login_api_router)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def home():
#     return {
#         "status": "Active",
#         "status_code": 200
#     }

def initialize_config():
    import os
    curr_dir = os.getcwd()
    cf.set_default_path(curr_dir)

if __name__ == "__main__":
    from core.service.config_service import read_config
    initialize_config()
    config = read_config()
    uvicorn.run(app, port=int(config['APPLICATION']['PORT']), host="0.0.0.0")