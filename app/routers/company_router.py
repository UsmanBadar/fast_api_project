import httpx
from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
from app.dependencies.redis_dependency import redis_cache
from app.dependencies.rate_limit_dependency import rate_limiter


company_router = APIRouter(prefix="/company")




@company_router.get("/latest_stock_price", dependencies=[Depends(rate_limiter)])
@redis_cache(expiry=300)
async def get_latest_stock_price(company_ticker: str):
    url = f"https://financialmodelingprep.com/stable/quote"
    params = {
        "symbol": company_ticker,
        "apikey": settings.FMP_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            
            response.raise_for_status() 
            
            data = response.json()
            
            if not data:
                raise HTTPException(status_code=404, detail="Ticker not found")
                
            return data
            
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error from data provider {exc}")
        except httpx.RequestError as req_exc:
            raise HTTPException(status_code=503, detail= f"Service unavailable {req_exc}")