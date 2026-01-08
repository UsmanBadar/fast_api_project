import httpx
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.company_fundamentals_service import get_or_fetch_company_fundamentals
from app.db_connection import get_db


company_fundamentals_router = APIRouter(prefix="/company_fundamentals", tags=["Company Fundamentals"])


@company_fundamentals_router.get("/{company_symbol}")
async def get_company_fundamentals(
    company_symbol: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        fundamentals = await get_or_fetch_company_fundamentals(
            company_symbol=company_symbol.upper(),
            db=db
        )
        if not fundamentals:
            raise HTTPException(
                status_code=404, 
                detail="No fundamentals found for the specified company symbol."
            )
        return {
            "data": fundamentals,
            "count": len(fundamentals)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")