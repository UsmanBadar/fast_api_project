import httpx
from fastapi import HTTPException
from app.schemas.company_balance_sheet_schema import CompanyBalanceSheetSchema
from app.core.config import settings





async def fetch_company_balance_sheet(symbol: str) -> CompanyBalanceSheetSchema:
    url = "https://financialmodelingprep.com/stable/balance-sheet-statement"
    params = {
        "symbol": symbol,
        "limit": 1,
        "apikey": settings.FMP_API_KEY,
    }

    try:

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            balance_sheet_data = result[0] if result else {}
            return CompanyBalanceSheetSchema(
                symbol=symbol,
                fiscal_year=int(balance_sheet_data.get("fiscalYear", "0000")),
                total_assets=balance_sheet_data.get("totalAssets", 0.0),
                total_liabilities=balance_sheet_data.get("totalLiabilities", 0.0),
                current_assets=balance_sheet_data.get("totalCurrentAssets", 0.0),
                current_liabilities=balance_sheet_data.get("totalCurrentLiabilities", 0.0),
                cash_and_cash_equivalents=balance_sheet_data.get("cashAndCashEquivalents", 0.0),
                long_term_debt=balance_sheet_data.get("longTermDebt", 0.0),
                total_equity=balance_sheet_data.get("totalStockholdersEquity", 0.0),
                debt_to_equity_ratio=(
                    balance_sheet_data.get("totalLiabilities", 0.0) /
                    balance_sheet_data.get("totalStockholdersEquity", 1.0)
                    if balance_sheet_data.get("totalStockholdersEquity", 0.0) != 0 else 0.0
                )
            )
    except Exception as e:
        raise HTTPException(500, detail=f"Error fetching the balance sheet: {e}")
        