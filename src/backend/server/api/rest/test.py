from fastapi import APIRouter, FastAPI

app = FastAPI()
router = APIRouter()

def resolver():
    return "hello world!"

app.get("/")(resolver)
# @app.get("/")
# def hello():
    # return resolver()   

# app.include_router(router, prefix="/hello")