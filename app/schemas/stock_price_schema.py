from pydantic import BaseModel, Field
from typing import List


class StockPriceRecord(BaseModel):
    """Individual stock price record for a specific date"""
    symbol: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Trading date")
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="Highest price of the day")
    low: float = Field(..., description="Lowest price of the day")
    close: float = Field(..., description="Closing price")
    volume: int = Field(..., description="Trading volume")
    change: float = Field(..., description="Price change")
    changePercent: float = Field(..., description="Percentage change")
    vwap: float = Field(..., description="Volume Weighted Average Price")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "date": "2025-12-31",
                "open": 273.06,
                "high": 273.68,
                "low": 271.75,
                "close": 271.86,
                "volume": 27293639,
                "change": -1.2,
                "changePercent": -0.43946,
                "vwap": 272.5875
            }
        }


class StockPriceAggregates(BaseModel):
    """Calculated aggregate values across all price records"""
    overall_high: float = Field(..., description="Highest price across all records")
    overall_low: float = Field(..., description="Lowest price across all records")
    average_volume: float = Field(..., description="Average trading volume across all records")


class StockPriceChartResponse(BaseModel):
    """Complete response with price data and calculated aggregates"""
    symbol: str = Field(..., description="Stock ticker symbol")
    data: List[StockPriceRecord] = Field(..., description="List of historical price records")
    aggregates: StockPriceAggregates = Field(..., description="Calculated aggregate statistics")
    record_count: int = Field(..., description="Total number of records returned")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "data": [
                    {
                        "symbol": "AAPL",
                        "date": "2025-12-31",
                        "open": 273.06,
                        "high": 273.68,
                        "low": 271.75,
                        "close": 271.86,
                        "volume": 27293639,
                        "change": -1.2,
                        "changePercent": -0.43946,
                        "vwap": 272.5875
                    }
                ],
                "aggregates": {
                    "overall_high": 274.08,
                    "overall_low": 271.75,
                    "average_volume": 24716628.0
                },
                "record_count": 2
            }
        }
