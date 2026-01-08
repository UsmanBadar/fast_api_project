from pydantic import BaseModel, Field
from typing import List
from app.schemas.portfolio_company_schema import PortfolioCompanySchema




class PorfolioCompanyWithSharePriceSchema(PortfolioCompanySchema):
    latest_share_price: float = Field(..., description="The latest share price of the company")

class PortfolioSchema(BaseModel):
    user_name: str = Field(..., description="The username associated with the portfolio")
    companies: List[PorfolioCompanyWithSharePriceSchema] = Field(
        default_factory=list,
        description="List of companies in the user's portfolio"
    )
    total_investment: float = Field(0.0, description="The total investment amount in the portfolio")
    total_current_value: float = Field(0.0, description="The total current value) of the portfolio")
    total_profit_loss: float = Field(0.0, description="The total profit or loss amount of the portfolio")
    total_profit_loss_percentage: float = Field(0.0, description="The total profit or loss percentage of the portfolio")

    class Config:
        from_attributes = True