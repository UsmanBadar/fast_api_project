from app.db_connection import Base
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

class PortfolioCompanyModel(Base):
    __table_args__ = {"schema": "dbo"}
    __tablename__ = "portfolio_companies"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(String)
    symbol: Mapped[str] = mapped_column(String)
    company_name: Mapped[str] = mapped_column(String)
    shares_owned: Mapped[int] = mapped_column(Integer, default=0)
    average_purchase_price: Mapped[float] = mapped_column(Float, default=0.0)
    total_investment: Mapped[float] = mapped_column(Float, default=0.0)
    current_price: Mapped[float] = mapped_column(Float, default=0.0)
    total_value: Mapped[float] = mapped_column(Float, default=0.0)
    profit_loss: Mapped[float] = mapped_column(Float, default=0.0)
    profit_loss_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String, default="USD")