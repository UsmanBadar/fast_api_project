from app.services.portfolio_service import get_portfolio_companies_with_share_price_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_connection import get_db
from app.schemas.portfolio_schema import PortfolioSchema


portfolio_router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@portfolio_router.post("/get_companies", response_model=PortfolioSchema)
async def get_portfolio_companies(user_name: str, db: AsyncSession = Depends(get_db)):

    result = await get_portfolio_companies_with_share_price_service(user_name, db)
    return PortfolioSchema(user_name=user_name, companies=result)