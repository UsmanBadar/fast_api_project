from fastapi import APIRouter
from app.services.company_balance_sheet_service import fetch_company_balance_sheet
from app.schemas.company_balance_sheet_schema import CompanyBalanceSheetSchema

company_balance_sheet_router = APIRouter(prefix="/company-balance-sheet", tags=["Company Balance Sheet"])


@company_balance_sheet_router.get("/{company_symbol}", response_model=CompanyBalanceSheetSchema)
async def get_company_balance_sheet(company_symbol: str) -> CompanyBalanceSheetSchema:
    return await fetch_company_balance_sheet(company_symbol)