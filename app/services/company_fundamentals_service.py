import httpx
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any
from app.models.company_fundamentals_model import CompanyFundamentalsModel

BASE_URL = "https://financialmodelingprep.com/stable"

async def fetch_income_statement(company_symbol: str, limit: int = 5) -> dict:
    try:
        url = f"{BASE_URL}/income-statement"
        params = {
            "symbol": company_symbol,
            "limit": limit,
            "period": "annual",
            "apikey": settings.FMP_API_KEY
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching income statement for {company_symbol}: {e}")
    
async def fetch_balance_sheet(company_symbol: str, limit: int = 5) -> dict:
    try:
        url = f"{BASE_URL}/balance-sheet-statement"
        params = {
            "symbol": company_symbol,
            "limit": limit,
            "period": "annual",
            "apikey": settings.FMP_API_KEY
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching balance sheet for {company_symbol}: {e}")
    
async def fetch_cash_flow_statement(company_symbol: str, limit: int = 5) -> dict:
    try:
        url = f"{BASE_URL}/cash-flow-statement"
        params = {
            "symbol": company_symbol,
            "limit": limit,
            "period": "annual",
            "apikey": settings.FMP_API_KEY
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching cash flow statement for {company_symbol}: {e}")
    

async def process_company_fundamentals(company_symbol: str) -> list[Dict[str, Any]]:
    try:
        income_statement = await fetch_income_statement(company_symbol)
        balance_sheet = await fetch_balance_sheet(company_symbol)
        cash_flow_statement = await fetch_cash_flow_statement(company_symbol)

        fundamentals = {}
        for statement in (income_statement, balance_sheet, cash_flow_statement):
            for record in statement:
                fiscal_year = int(record.get("fiscalYear", 0))
                if fiscal_year not in fundamentals:
                    fundamentals[fiscal_year] = {"fiscal_year": fiscal_year}
                if statement is income_statement:
                    fundamentals[fiscal_year].update({
                        "revenue": record.get("revenue", None),
                        "gross_profit": record.get("grossProfit", None),
                        "operating_income": record.get("operatingIncome", None),
                        "net_income": record.get("netIncome", None),
                        "earnings_per_share": record.get("eps", None),
                    })
                elif statement is balance_sheet:
                    fundamentals[fiscal_year].update({
                        "total_assets": record.get("totalAssets", None),
                        "total_liabilities": record.get("totalLiabilities", None),
                        "reporting_currency": record.get("reportedCurrency", None),
                    })
                elif statement is cash_flow_statement:
                    fundamentals[fiscal_year].update({
                        "operating_cash_flow": record.get("operatingCashFlow", None),
                        "free_cash_flow": record.get("freeCashFlow", None),
                        "capital_expenditures": record.get("capitalExpenditure", None),
                    })
        return list(fundamentals.values())
    except Exception as e:
        raise RuntimeError(f"Error processing company fundamentals for {company_symbol}: {e}")
    

async def upsert_company_fundamentals(
    db: AsyncSession,
    company_symbol: str,
    fundamentals: list[dict]
):
    for record in fundamentals:
        fiscal_year = record["fiscal_year"]

        stmt = select(CompanyFundamentalsModel).where(
            CompanyFundamentalsModel.company_symbol == company_symbol,
            CompanyFundamentalsModel.fiscal_year == fiscal_year
        )

        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            for field, value in record.items():
                if hasattr(existing, field):
                    setattr(existing, field, value)
        else:
            db.add(
                CompanyFundamentalsModel(
                    company_symbol=company_symbol,
                    **record
                )
            )

    await db.commit()
