import httpx
from fastapi import HTTPException
from app.core.config import settings



async def fetch_stock_target_price(ticker: str) -> dict[str, any]:
    try:
        url = "https://financialmodelingprep.com/stable/price-target-consensus"

        params = {
            "symbol": ticker,
            "apikey": settings.FMP_API_KEY
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise HTTPException(status_code=404, detail="No target price data found for the given ticker.")
        return data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock target price: {str(e)}")