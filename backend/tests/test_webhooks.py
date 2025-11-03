# tests/test_webhooks.py
import asyncio
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import database, transactions
import time

@pytest.fixture(autouse=True)
async def prepare_db():
    # Ensure DB connected and clear table before tests
    await database.connect()
    await database.execute(transactions.delete())  # clear
    yield
    await database.execute(transactions.delete())
    await database.disconnect()

@pytest.mark.asyncio
async def test_single_transaction_processing():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "transaction_id": "txn_test_single",
            "source_account": "acc_user_1",
            "destination_account": "acc_m_1",
            "amount": 100.0,
            "currency": "INR"
        }
        r = await ac.post("/v1/webhooks/transactions", json=payload)
        assert r.status_code == 202
        # Immediately check status: should be PROCESSING
        r2 = await ac.get("/v1/transactions/txn_test_single")
        assert r2.status_code == 200
        assert r2.json()["status"] in ("PROCESSING", "PROCESSED")
        # Wait 35 seconds to allow processing to finish
        await asyncio.sleep(35)
        r3 = await ac.get("/v1/transactions/txn_test_single")
        assert r3.status_code == 200
        assert r3.json()["status"] == "PROCESSED"

@pytest.mark.asyncio
async def test_idempotency_duplicate_requests():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "transaction_id": "txn_test_dup",
            "source_account": "acc_user_dup",
            "destination_account": "acc_m_dup",
            "amount": 50.0,
            "currency": "INR"
        }
        # send same webhook multiple times quickly
        r1 = await ac.post("/v1/webhooks/transactions", json=payload)
        r2 = await ac.post("/v1/webhooks/transactions", json=payload)
        assert r1.status_code == 202
        assert r2.status_code == 202
        # There should be only one row in DB with that transaction_id
        query = transactions.select().where(transactions.c.transaction_id == "txn_test_dup")
        rows = await database.fetch_all(query)
        assert len(rows) == 1
        # wait for processing
        await asyncio.sleep(35)
        row = await database.fetch_one(query)
        assert row["status"] == "PROCESSED"
