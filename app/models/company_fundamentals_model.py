from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db_connection import Base

class CompanyFundamentalsModel(Base):
    __table_args__ = (UniqueConstraint('company_symbol', 'fiscal_year', name='uq_company_fiscal_year'), {"schema": "dbo"})
    __tablename__ = "company_fundamentals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_symbol: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    fiscal_year: Mapped[int] = mapped_column(Integer, nullable=False)
    reporting_currency: Mapped[str | None] = mapped_column(String(5), nullable=True)

    revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    gross_profit: Mapped[float | None] = mapped_column(Float, nullable=True)
    operating_income: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_income: Mapped[float | None] = mapped_column(Float, nullable=True)

    operating_cash_flow: Mapped[float | None] = mapped_column(Float, nullable=True)
    free_cash_flow: Mapped[float | None] = mapped_column(Float, nullable=True)
    capital_expenditures: Mapped[float | None] = mapped_column(Float, nullable=True)

    earnings_per_share: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_assets: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_liabilities: Mapped[float | None] = mapped_column(Float, nullable=True)