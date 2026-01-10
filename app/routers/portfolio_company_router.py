from app.services.portfolio_service import add_portfolio_company_service, remove_portfolio_company_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_connection import get_db
from app.schemas.portfolio_company_schema import PortfolioCompanySchema


portfolio_company_router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@portfolio_company_router.post("/add/company")
async def add_portfolio_company(
    company: PortfolioCompanySchema,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await add_portfolio_company_service(company.user_name, company, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add company to portfolio: {e}")
    


@portfolio_company_router.delete("/remove/company/{company_symbol}")
async def remove_portfolio_company(
    company_symbol: str,
    user_name: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await remove_portfolio_company_service(user_name, company_symbol, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove company from portfolio: {e}")
