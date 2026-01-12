import httpx
from fastapi import HTTPException
from app.schemas.company_profile_schema import CompanyProfileSchema
from app.core.config import settings



async def fetch_company_profile(symbol: str) -> CompanyProfileSchema:

    company_profile_api_url = "https://financialmodelingprep.com/stable/profile"
    company_profile_params = {
        "symbol": symbol,
        "apikey": settings.FMP_API_KEY
    }
    company_revenue_api_url = "https://financialmodelingprep.com/stable/revenue-geographic-segmentation"
    company_revenue_params = {
        "symbol": symbol,
        "period": "annual",
        "structure": "flat",
        "apikey": settings.FMP_API_KEY
    }

    try:
        async with httpx.AsyncClient() as client:
            profile_response = await client.get(company_profile_api_url, params=company_profile_params)
            profile_response.raise_for_status()
            profile_result = profile_response.json()
            profile_data = profile_result[0] 

            revenue_response = await client.get(company_revenue_api_url, params=company_revenue_params)
            revenue_response.raise_for_status()
            revenue_result = revenue_response.json()
            revenue_data = revenue_result[0]
            return CompanyProfileSchema(
                company_name=profile_data.get("companyName", ""),
                website=profile_data.get("website", ""),
                description=profile_data.get("description", ""),
                industry=profile_data.get("industry", ""),
                sector=profile_data.get("sector", ""),
                country=profile_data.get("country", ""),
                ceo=profile_data.get("ceo", ""),
                exchange_full_name=profile_data.get("exchangeFullName", ""),
                symbol=profile_data.get("symbol", ""),
                market_cap=profile_data.get("marketCap", 0),
                currency=profile_data.get("currency", ""),
                cik=profile_data.get("cik", ""),
                isin=profile_data.get("isin", ""),
                ipo_date=profile_data.get("ipoDate", ""),
                revenue_by_regions=revenue_data.get("data", {})
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching company profile: {str(e)}")

    
    
    