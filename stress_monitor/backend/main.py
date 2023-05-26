import sys
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

sys.path.append("")
from backend import prediction_api_router, monitor_api_router, login_api_router

app = FastAPI()
app.include_router(prediction_api_router)
app.include_router(monitor_api_router)
app.include_router(login_api_router)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    from backend.utils.application_utils import *
    from backend import config
    print("#"*25," SETTINGS ","#"*25,"\n",config._sections)
    uvicorn.run(app, port=int(config['APPLICATION']['port']), host="0.0.0.0")