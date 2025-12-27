from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company_fundamentals_metrics_model import CompanyFundamentalMetricsModel
from app.schemas.company_fundamental_metrics_pydantic_model import CompanyFundamentalMetricSchema

async def get_company_fundamental_metrics(
    db: AsyncSession,
    company_symbol: str
):
    stmt = (
        select(CompanyFundamentalMetricsModel)
        .where(CompanyFundamentalMetricsModel.company_symbol == company_symbol)
        .order_by(CompanyFundamentalMetricsModel.fiscal_year)
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()

    return [
        CompanyFundamentalMetricSchema
        .model_validate(row)
        .model_dump()
        for row in rows
    ]

