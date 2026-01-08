from pydantic import BaseModel, Field
from typing import Optional



class PortfolioCompanySchema(BaseModel):
    user_name: str = Field(..., description="The email associated with the portfolio company")
    symbol: str = Field(..., description="The stock symbol of the portfolio company")
    company_name: str = Field(..., description="The name of the portfolio company")
    shares_owned: int = Field(0, description="The number of shares owned")
    average_purchase_price: float = Field(0.0, description="The average purchase price of the shares")
    total_investment: float = Field(0.0, description="The total investment amount")
    current_price: float = Field(0.0, description="The current price of the stock")
    total_value: float = Field(0.0, description="The total current value of the shares")
    profit_loss: float = Field(0.0, description="The profit or loss amount")
    profit_loss_percentage: float = Field(0.0, description="The profit or loss percentage")
    currency: str = Field("USD", description="The currency of the investment")