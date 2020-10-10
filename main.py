# Has to be called main.py because 
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker expects it
from fastapi import FastAPI

app = FastAPI()


from api.routes import router
app.include_router(router)