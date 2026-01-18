from pydantic import BaseModel, Field


class CompanyBalanceSheetSchema(BaseModel):
    symbol: str = Field(..., description="The stock symbol of the company")
    fiscal_year: int = Field(..., description="The fiscal year of the balance sheet")
    total_assets: float = Field(0.0, description="The total assets of the company")
    total_liabilities: float = Field(0.0, description="The total liabilities of the company")
    current_assets: float = Field(0.0, description="The current assets of the company")
    current_liabilities: float = Field(0.0, description="The current liabilities of the company")
    cash_and_cash_equivalents: float = Field(0.0, description="The cash and cash equivalents of the company")
    long_term_debt: float = Field(0.0, description="The long-term debt of the company")
    total_equity: float = Field(0.0, description="The total equity of the company")
    debt_to_equity_ratio: float = Field(0.0, description="The debt to equity ratio of the company")
