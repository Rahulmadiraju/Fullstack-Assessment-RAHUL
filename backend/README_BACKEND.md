# Backend - Full Stack Developer Assessment

Written by Rahul M — internship assessment project

This backend is a FastAPI application that accepts transaction webhooks and processes them in the background
with idempotency guarantees and persistent storage (SQLite by default, but easily switched to Postgres).

Key endpoints:
- `GET /` - health check
- `POST /v1/webhooks/transactions` - webhook receiver (returns 202 Accepted, responds quickly)
- `GET /v1/transactions/{transaction_id}` - retrieve stored transaction status

Run locally (Windows PowerShell):
PS> cd backend
PS> python -m venv .venv
PS> .\.venv\Scripts\Activate.ps1
PS> pip install -r requirements.txt
PS> uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Notes:
- Uses SQLite for local persistence (file: transactions.db).
- Simulates processing taking 30 seconds (asyncio.sleep).
- Idempotency: if a transaction_id exists and is processed or processing, it will not start duplicate processing.
- Includes pytest tests.
