import httpx
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, and_
from datetime import date, datetime, timedelta
from typing import Dict, Any, List, Union, Optional
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
            result = response.json()
            income_statements = []
            for record in result:
                income_statements.append({
                    "date": date.fromisoformat(record.get("date")) if record.get("date") else None,
                    "fiscal_year": record.get("fiscalYear", None),
                    "company_symbol": record.get("symbol", None),
                    "revenue": record.get("revenue", None),
                    "gross_profit": record.get("grossProfit", None),
                    "net_income": record.get("netIncome", None),
                    "eps": record.get("eps", None),
                    "reporting_currency": record.get("reportedCurrency", None)
                })
            return income_statements
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching income statement for {company_symbol}: {e}")
    

async def fetch_financial_ratios(company_symbol: str, limit : int = 5):
    try:
        url = f"{BASE_URL}/ratios"
        params = {
            "symbol": company_symbol,
            "limit": limit,
            "period": "annual",
            "apikey": settings.FMP_API_KEY
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params= params)
            resp.raise_for_status()
            result = resp.json()

            financial_ratios = []
            for record in result:
                financial_ratios.append({
                    "fiscal_year": record.get("fiscalYear", None),
                    "price_to_earings_ratio": record.get("priceToEarningsRatio", None),
                    "price_to_book_ratio": record.get("priceToBookRatio", None),
                    "price_to_sales_ratio": record.get("priceToSalesRatio", None),
                    "reporting_currency": record.get("reportedCurrency", None)
                })
            return financial_ratios
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching the financial ratios for {company_symbol}. Error: {e}")
    

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
            result = response.json()
            balance_sheets = []
            for record in result:
                balance_sheets.append({
                    "fiscal_year": record.get("fiscalYear", None),
                    "total_assets": record.get("totalAssets", None),
                    "total_liabilities": record.get("totalLiabilities", None),
                    "reporting_currency": record.get("reportedCurrency", None)
                })
            return balance_sheets
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
            result = response.json()

            cash_flow_statements = []
            for record in result:
                cash_flow_statements.append({
                    "fiscal_year": record.get("fiscalYear", None),
                    "free_cash_flow": record.get("freeCashFlow", None),
                    "reporting_currency": record.get("reportedCurrency", None)
                })
            return cash_flow_statements
    except httpx.HTTPError as e:
        raise RuntimeError(f"Error fetching cash flow statement for {company_symbol}: {e}")


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _calc_pct_change(prev_value: Any, curr_value: Any) -> Optional[float]:
    if not _is_number(prev_value) or not _is_number(curr_value):
        return None
    if prev_value == 0:
        return None
    return ((curr_value - prev_value) / prev_value) * 100.0


def _safe_year(v: Any) -> int:
    try:
        return int(v)
    except Exception:
        return 10**9  
    

def calc_yoy_metrics(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    sorted_data = sorted(data, key=lambda d: _safe_year(d.get("fiscal_year")))

    prev: Optional[Dict[str, Any]] = None
    suffix = "_yoy_pct"
    metrics = ["revenue", "gross_profit", "net_income", "free_cash_flow"]

    for record in sorted_data:
        if prev is None:
            for metric in metrics:
                record[f"{metric}{suffix}"] = None
            prev = record
            continue

        for metric in metrics:
            pct_change = _calc_pct_change(prev.get(metric), record.get(metric))
            record[f"{metric}{suffix}"] = pct_change

        prev = record

    return sorted_data
    

async def process_company_fundamentals(company_symbol: str) -> list[Dict[str, Any]]:
    try:
        income_statement = await fetch_income_statement(company_symbol)
        cash_flow_statement = await fetch_cash_flow_statement(company_symbol)
        financial_ratios = await fetch_financial_ratios(company_symbol)

        cash_flow_statement_index = {
            (record["fiscal_year"], record["reporting_currency"]): record for record in cash_flow_statement
        }

        financial_ratios_index = {
            (record["fiscal_year"], record["reporting_currency"]): record for record in financial_ratios
        }

        fundamentals = []

        for record in income_statement:
            fiscal_year = record["fiscal_year"]
            reporting_currency = record.get("reporting_currency")

            key = (fiscal_year, reporting_currency)

            cash_flow_record = cash_flow_statement_index.get(key, {})
            ratio_record = financial_ratios_index.get(key, {})

            combined_record = {
                "fiscal_year": fiscal_year,
                "date": record.get("date"),
                "symbol": record.get("company_symbol"),    
                "revenue": record.get("revenue"),
                "gross_profit": record.get("gross_profit"),
                "net_income": record.get("net_income"),
                "eps": record.get("eps"),
                "free_cash_flow": cash_flow_record.get("free_cash_flow"),
                "price_to_earings_ratio": ratio_record.get("price_to_earings_ratio"),
                "price_to_book_ratio": ratio_record.get("price_to_book_ratio"),
                "price_to_sales_ratio": ratio_record.get("price_to_sales_ratio"),
                "reporting_currency": reporting_currency,
            }

            fundamentals.append(combined_record)

        return calc_yoy_metrics(fundamentals)

    except Exception as e:
        raise RuntimeError(f"Error processing company fundamentals for {company_symbol}: {e}")


async def is_data_fresh(company_symbol: str, db: AsyncSession) -> bool:
    try:
        stmt = select(func.max(CompanyFundamentalsModel.date)).where(
            CompanyFundamentalsModel.company_symbol == company_symbol,
            CompanyFundamentalsModel.date.isnot(None)
        )
        result = await db.execute(stmt)
        latest_date = result.scalar_one_or_none()
        
        if latest_date is None:
            return False
        
        # Data is fresh if the latest record is less than 1 year old
        one_year_ago = datetime.now().date() - timedelta(days=365)
        return latest_date >= one_year_ago
    except Exception as e:
        raise RuntimeError(f"Error checking data freshness for {company_symbol}: {e}")


async def upsert_company_fundamentals(
    company_symbol: str, 
    fundamentals_data: List[Dict[str, Any]], 
    db: AsyncSession
) -> Dict[str, Any]:
    try:
        if not fundamentals_data:
            return {"inserted": 0}
        
        stmt = select(CompanyFundamentalsModel).where(
            CompanyFundamentalsModel.company_symbol == company_symbol
        )
        result = await db.execute(stmt)
        existing_records = result.scalars().all()
        
        existing_map = {record.fiscal_year: record for record in existing_records}
        
        records_to_insert = []
        
        for record in fundamentals_data:
            fiscal_year = record.get("fiscal_year")
            record_data = {
                "company_symbol": record.get("symbol", company_symbol),
                "fiscal_year": fiscal_year,
                "date": record.get("date"),
                "revenue": record.get("revenue"),
                "revenue_yoy_change": record.get("revenue_yoy_pct"),
                "gross_profit": record.get("gross_profit"),
                "gross_profit_yoy_change": record.get("gross_profit_yoy_pct"),
                "net_income": record.get("net_income"),
                "net_income_yoy_change": record.get("net_income_yoy_pct"),
                "free_cash_flow": record.get("free_cash_flow"),
                "free_cash_flow_yoy_change": record.get("free_cash_flow_yoy_pct"),
                "eps": record.get("eps"),
                "price_to_earings_ratio": record.get("price_to_earings_ratio"),
                "price_to_book_ratio": record.get("price_to_book_ratio"),
                "price_to_sales_ratio": record.get("price_to_sales_ratio"),
                "reporting_currency": record.get("reporting_currency")
            }
            
            if fiscal_year in existing_map:
                pass
            else:
                records_to_insert.append(record_data)
        
        
        if records_to_insert:
            db.add_all([CompanyFundamentalsModel(**data) for data in records_to_insert])
        
        await db.commit()
        
        return {
            "company_symbol": company_symbol,
            "inserted": len(records_to_insert),
            "status": "success"
        }
    except Exception as e:
        await db.rollback()
        raise RuntimeError(f"Error upserting company fundamentals for {company_symbol}: {e}")


async def get_or_fetch_company_fundamentals(
    company_symbol: str, 
    db: AsyncSession,
) -> List[Dict[str, Any]]:
    try:
        if await is_data_fresh(company_symbol, db):
            stmt = select(CompanyFundamentalsModel).where(
                CompanyFundamentalsModel.company_symbol == company_symbol
            ).order_by(CompanyFundamentalsModel.fiscal_year.desc())
            
            result = await db.execute(stmt)
            records = result.scalars().all()
            
            return [
                {
                    "fiscal_year": record.fiscal_year,
                    "date": record.date,
                    "symbol": record.company_symbol,
                    "revenue": record.revenue,
                    "revenue_yoy_change": record.revenue_yoy_change,
                    "gross_profit": record.gross_profit,
                    "gross_profit_yoy_change": record.gross_profit_yoy_change,
                    "net_income": record.net_income,
                    "net_income_yoy_change": record.net_income_yoy_change,
                    "free_cash_flow": record.free_cash_flow,
                    "free_cash_flow_yoy_change": record.free_cash_flow_yoy_change,
                    "eps": record.eps,
                    "price_to_earings_ratio": record.price_to_earings_ratio,
                    "price_to_book_ratio": record.price_to_book_ratio,
                    "price_to_sales_ratio": record.price_to_sales_ratio,
                    "reporting_currency": record.reporting_currency
                }
                for record in records
            ]
        
        fundamentals_data = await process_company_fundamentals(company_symbol)
        
        await upsert_company_fundamentals(company_symbol, fundamentals_data, db)
        
        return fundamentals_data
    except Exception as e:
        raise RuntimeError(f"Error getting or fetching company fundamentals for {company_symbol}: {e}")
