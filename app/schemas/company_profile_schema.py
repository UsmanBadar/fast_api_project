from pydantic import BaseModel, Field

class CompanyProfileSchema(BaseModel):
    company_name: str = Field(..., title="Company Name", description="The name of the company")
    website: str = Field(None, title="Website", description="The website URL of the company") 
    description: str = Field(..., title="Description", description="A brief description of the company")
    industry: str = Field(..., title="Industry", description="The industry the company operates in")
    sector: str = Field(..., title="Sector", description="The sector the company belongs to")
    country: str = Field(..., title="Country", description="The country where the company is located")
    ceo: str = Field(..., title="CEO", description="The name of the company's CEO")
    exchange_full_name: str = Field(..., title="Exchange Full Name", description="The full name of the stock exchange")
    symbol: str = Field(..., title="Symbol", description="The stock symbol of the company")
    market_cap: float = Field(..., title="Market Capitalization", description="The market capitalization of the company")
    currency: str = Field(..., title="Currency", description="The currency used for the company's stock")
    cik: str = Field(..., title="CIK", description="The Central Index Key of the company")
    isin: str = Field(..., title="ISIN", description="The International Securities Identification Number of the company")
    ipo_date: str = Field(None, title="IPO Date", description="The IPO date of the company")
    revenue_by_regions: dict = Field(None, title="Revenue by Regions", description="A dictionary representing the company's revenue by regions")