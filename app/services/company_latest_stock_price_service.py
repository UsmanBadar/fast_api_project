import httpx
from fastapi import HTTPException
from app.core.config import settings





async def get_latest_company_stock_price_service(company_ticker: str):
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