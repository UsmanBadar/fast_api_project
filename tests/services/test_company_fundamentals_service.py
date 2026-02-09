import asyncio
import sys
import types

fake_model_module = types.ModuleType("app.models.company_fundamentals_model")
fake_model_module.CompanyFundamentalsModel = type("CompanyFundamentalsModel", (), {})
sys.modules.setdefault("app.models.company_fundamentals_model", fake_model_module)

from app.services import company_fundamentals_service as svc


def test_calc_yoy_metrics_sorts_and_computes_percentage_change():
    records = [
        {"fiscal_year": 2024, "revenue": 110, "gross_profit": 55, "net_income": 22, "free_cash_flow": 11},
        {"fiscal_year": 2023, "revenue": 100, "gross_profit": 50, "net_income": 20, "free_cash_flow": 10},
    ]

    result = svc.calc_yoy_metrics(records)

    assert result[0]["fiscal_year"] == 2023
    assert result[0]["revenue_yoy_pct"] is None
    assert result[1]["revenue_yoy_pct"] == 10.0


def test_process_company_fundamentals_merges_statement_sources(monkeypatch):
    async def fake_income(symbol):
        return [{"fiscal_year": 2024, "date": None, "company_symbol": symbol, "revenue": 100, "gross_profit": 50, "net_income": 30, "eps": 2.5, "reporting_currency": "USD"}]

    async def fake_cashflow(symbol):
        return [{"fiscal_year": 2024, "free_cash_flow": 20, "reporting_currency": "USD"}]

    async def fake_ratios(symbol):
        return [{"fiscal_year": 2024, "price_to_earings_ratio": 25, "price_to_book_ratio": 5, "price_to_sales_ratio": 3, "reporting_currency": "USD"}]

    monkeypatch.setattr(svc, "fetch_income_statement", fake_income)
    monkeypatch.setattr(svc, "fetch_cash_flow_statement", fake_cashflow)
    monkeypatch.setattr(svc, "fetch_financial_ratios", fake_ratios)

    result = asyncio.run(svc.process_company_fundamentals("AAPL"))

    assert result[0]["symbol"] == "AAPL"
    assert result[0]["free_cash_flow"] == 20
    assert result[0]["price_to_earings_ratio"] == 25
