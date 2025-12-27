from pydantic import BaseModel

class CompanyFundamentalMetricSchema(BaseModel):
    fiscal_year: int
    revenue: float | None
    gross_profit: float | None
    net_income: float | None
    free_cash_flow: float | None

    gross_margin: float | None
    net_margin: float | None
    fcf_margin: float | None

    revenue_yoy_growth: float | None
    net_income_yoy_growth: float | None
    fcf_yoy_growth: float | None

    class Config:
        from_attributes = True
