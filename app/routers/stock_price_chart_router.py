import httpx
import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.core.config import settings
from app.dependencies.redis_dependency import redis_cache
from app.dependencies.rate_limit_dependency import rate_limiter
from app.schemas.stock_price_schema import (
    StockPriceChartResponse,
    StockPriceRecord,
    StockPriceAggregates
)


stock_price_chart_router = APIRouter(prefix="/stock_chart", tags=["Stock Chart"])


@stock_price_chart_router.get("/{company_symbol}", response_model=StockPriceChartResponse, dependencies=[Depends(rate_limiter)])
@redis_cache(expiry=14400)
async def get_stock_chart(company_symbol: str):

    url = f"https://financialmodelingprep.com/stable/historical-price-eod/full"

    current_month = datetime.date.today().month
    previous_fourth_month = current_month - 4
    if current_month <= 4:
        previous_fourth_month += 12
        year = datetime.date.today().year - 1
    else:
        year = datetime.date.today().year

    four_month_old_date = datetime.date(year, previous_fourth_month, datetime.date.today().day)


    params = {
        "symbol": company_symbol,
        "from": four_month_old_date.isoformat(),
        "to": datetime.date.today().isoformat(),
        "apikey": settings.FMP_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            
            response.raise_for_status() 
            
            data = response.json()
            
            if not data:
                raise HTTPException(status_code=404, detail="Ticker not found")
            
            price_records = [StockPriceRecord(**record) for record in data]
            
            if price_records:
                overall_high = max(record.high for record in price_records)
                overall_low = min(record.low for record in price_records)
                average_volume = sum(record.volume for record in price_records) / len(price_records)
                
                aggregates = StockPriceAggregates(
                    overall_high=overall_high,
                    overall_low=overall_low,
                    average_volume=average_volume
                )
            else:
                aggregates = StockPriceAggregates(
                    overall_high=0.0,
                    overall_low=0.0,
                    average_volume=0.0
                )
            
            return StockPriceChartResponse(
                symbol=company_symbol,
                data=price_records,
                aggregates=aggregates,
                record_count=len(price_records)
            )
            
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Error from data provider {exc}")
        except httpx.RequestError as req_exc:
            raise HTTPException(status_code=503, detail= f"Service unavailable {req_exc}")