from fastapi import APIRouter
from app.services.company_profile_service import fetch_company_profile
from app.schemas.company_profile_schema import CompanyProfileSchema


company_profile_router = APIRouter(prefix="/company_profile", tags=["Company Profile"])


@company_profile_router.get("/{company_symbol}", response_model=CompanyProfileSchema)
async def get_company_profile(company_symbol: str) -> CompanyProfileSchema:
    return await fetch_company_profile(company_symbol)
    