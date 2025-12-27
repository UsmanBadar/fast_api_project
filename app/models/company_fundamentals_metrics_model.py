from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db_connection import Base

class CompanyFundamentalMetricsModel(Base):
    __tablename__ = "company_fundamental_metrics"
    __table_args__ = {"schema": "dbo"}

    company_symbol: Mapped[str] = mapped_column(String(10), primary_key=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, primary_key=True)

    revenue: Mapped[float | None] = mapped_column(Float)
    gross_profit: Mapped[float | None] = mapped_column(Float)
    net_income: Mapped[float | None] = mapped_column(Float)
    free_cash_flow: Mapped[float | None] = mapped_column(Float)

    gross_margin: Mapped[float | None] = mapped_column(Float)
    net_margin: Mapped[float | None] = mapped_column(Float)
    fcf_margin: Mapped[float | None] = mapped_column(Float)

    revenue_yoy_growth: Mapped[float | None] = mapped_column(Float)
    net_income_yoy_growth: Mapped[float | None] = mapped_column(Float)
    fcf_yoy_growth: Mapped[float | None] = mapped_column(Float)
