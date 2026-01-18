from sqlalchemy import Integer, String, Float, UniqueConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.db_connection import Base

class CompanyFundamentalsModel(Base):
    __table_args__ = (UniqueConstraint('company_symbol', 'fiscal_year', name='uq_company_fiscal_year'), {"schema": "dbo"})
    __tablename__ = "company_fundamentals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_symbol: Mapped[str] = mapped_column(String(20), index=True)
    fiscal_year: Mapped[str] = mapped_column(String(10), nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=True)
    revenue: Mapped[float] = mapped_column(Float, nullable=True)
    revenue_yoy_change: Mapped[float] = mapped_column(Float, nullable=True)
    gross_profit: Mapped[float] = mapped_column(Float, nullable=True)
    gross_profit_yoy_change: Mapped[float] = mapped_column(Float, nullable=True)
    net_income: Mapped[float] = mapped_column(Float, nullable=True)
    net_income_yoy_change: Mapped[float] = mapped_column(Float, nullable=True)
    free_cash_flow: Mapped[float] = mapped_column(Float, nullable=True)
    free_cash_flow_yoy_change: Mapped[float] = mapped_column(Float, nullable=True)
    eps: Mapped[float] = mapped_column(Float, nullable=True)
    price_to_earings_ratio: Mapped[float] = mapped_column(Float, nullable=True)
    price_to_book_ratio: Mapped[float] = mapped_column(Float, nullable=True)
    price_to_sales_ratio: Mapped[float] = mapped_column(Float, nullable=True)      
    reporting_currency: Mapped[str] = mapped_column(String, nullable=True)