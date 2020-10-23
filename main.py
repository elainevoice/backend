# Has to be called main.py because 
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker expects it
from fastapi import FastAPI

app = FastAPI(title="Elaine Voice API", description="Visit <URL>/docs for docs",)
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routes import router
app.include_router(router)