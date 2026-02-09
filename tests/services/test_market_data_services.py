import asyncio

import httpx

from app.services.company_latest_stock_price_service import get_latest_company_stock_price_service
from app.services.stock_target_price_service import fetch_stock_target_price


class DummyResponse:
    def __init__(self, payload, should_raise=False):
        self._payload = payload
        self._raise = should_raise
        self.status_code = 500

    def raise_for_status(self):
        if self._raise:
            raise httpx.HTTPStatusError(self)

    def json(self):
        return self._payload


class DummyClient:
    def __init__(self, payload, should_raise=False):
        self.payload = payload
        self.should_raise = should_raise

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, url, params=None):
        return DummyResponse(self.payload, should_raise=self.should_raise)


def test_get_latest_company_stock_price_service_returns_payload(monkeypatch):
    monkeypatch.setattr(httpx, "AsyncClient", lambda: DummyClient([{"symbol": "AAPL", "price": 190.1}]))

    result = asyncio.run(get_latest_company_stock_price_service("AAPL"))

    assert result[0]["symbol"] == "AAPL"


def test_fetch_stock_target_price_returns_first_record(monkeypatch):
    monkeypatch.setattr(httpx, "AsyncClient", lambda: DummyClient([{"targetHigh": 250, "targetLow": 180}]))

    result = asyncio.run(fetch_stock_target_price("AAPL"))

    assert result["targetHigh"] == 250
