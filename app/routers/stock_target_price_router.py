from fastapi import APIRouter, HTTPException
from app.services.stock_target_price_service import fetch_stock_target_price

stock_target_price_router = APIRouter(prefix="/stock-target-price", tags=["Stock Target Price"])

@stock_target_price_router.get("/{company_symbol}", summary="Get stock target price data for a given ticker")
async def get_stock_target_price(company_symbol: str):
    try:
        target_price_data = await fetch_stock_target_price(company_symbol)
        return target_price_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")