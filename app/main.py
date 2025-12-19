from fastapi import FastAPI
from app.routers import auth_router


app = FastAPI()

app.include_router(auth_router.auth_router)




@app.get("/")
async def home():
    return "Hello World!"




    