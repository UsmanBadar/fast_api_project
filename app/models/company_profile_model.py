from app.db_connection import Base
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

class CompanyProfileModel(Base):
    __table_args__ = {"schema": "dbo"}
    __tablename__ = "company_profiles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String)
    market_cap: Mapped[int] = mapped_column(Integer)
    last_dividend: Mapped[float] = mapped_column(Float)
    average_volume: Mapped[int] = mapped_column(Integer)
    company_name: Mapped[str] = mapped_column(String)                   
    currency: Mapped[str]   = mapped_column(String)
    cik: Mapped[str] = mapped_column(String)
    isin: Mapped[str] = mapped_column(String)
    exchange_full_name: Mapped[str] = mapped_column(String)
    industry: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    ceo: Mapped[str] = mapped_column(String)
    sector: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)


