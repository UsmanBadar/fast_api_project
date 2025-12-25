from fastapi import FastAPI
from app.routers import auth_router, company_router


app = FastAPI()

app.include_router(auth_router.auth_router)
app.include_router(company_router.company_router)




@app.get("/")
async def home():
    return "Hello World!"




    