import asyncio

import httpx

from app.routers.company_search_router import search_company_by_ticker


class DummyResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


class DummyClient:
    def __init__(self, payload):
        self.payload = payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, url, params=None):
        return DummyResponse(self.payload)


def test_search_company_by_ticker_filters_to_supported_exchanges(monkeypatch):
    payload = [
        {"symbol": "AAPL", "exchange": "NASDAQ"},
        {"symbol": "BHP", "exchange": "ASX"},
        {"symbol": "XYZ", "exchange": "NYSE"},
    ]
    monkeypatch.setattr(httpx, "AsyncClient", lambda: DummyClient(payload))

    result = asyncio.run(search_company_by_ticker("apple"))

    symbols = {company["symbol"] for company in result}
    assert symbols == {"AAPL", "BHP"}
