from fastapi import APIRouter, Depends
from app.services.ai_service.ai_service import run_ai_service
from app.db_connection import get_db
from app.dependencies.redis_dependency import redis_cache



ai_router = APIRouter(prefix="/ai", tags=["AI Services"])


@ai_router.get("/analyze/{company_symbol}")
@redis_cache(expiry=86400)
async def analyze_company(company_symbol: str, db=Depends(get_db)):

    analysis = await run_ai_service(company_symbol, db)
    return analysis