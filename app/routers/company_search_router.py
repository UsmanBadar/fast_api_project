import httpx
from fastapi import APIRouter, HTTPException
from app.core.config import settings


company_search_router = APIRouter(prefix="/company_search", tags=["Company Search"])
@company_search_router.get("/{company_name}")
async def search_company_by_ticker(company_name: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://financialmodelingprep.com/stable/search-name", params={
                    "query": company_name,
                    "apikey": settings.FMP_API_KEY
                })
            data = response.json()
            if not data:
                raise HTTPException(status_code=404, detail="No Company found")
            
            filtered_data = [stock for stock in data if stock.get("exchange") in ["ASX", "NASDAQ"]]
            
            if not filtered_data:
                raise HTTPException(status_code=404, detail="No Company found in ASX or NASDAQ exchanges")
            
            return filtered_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
