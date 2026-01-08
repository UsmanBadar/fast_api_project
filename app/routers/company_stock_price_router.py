import httpx
from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
from app.dependencies.redis_dependency import redis_cache
from app.dependencies.rate_limit_dependency import rate_limiter
from app.services.company_latest_stock_price_service import get_latest_company_stock_price_service


company_stock_price_router = APIRouter(prefix="/latest_stock_price", tags=["Company Stock Price"])




@company_stock_price_router.get("/{company_ticker}", dependencies=[Depends(rate_limiter)])
@redis_cache(expiry=300)
async def get_latest_stock_price(company_ticker: str):
    return await get_latest_company_stock_price_service(company_ticker)
    