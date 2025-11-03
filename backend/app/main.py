from fastapi import FastAPI, BackgroundTasks, HTTPException, status, Request
from fastapi.responses import JSONResponse
from .database import database
from .schemas import WebhookIn, TransactionOut
from .crud import create_processing, get_transaction
from .worker import process_transaction_job
from .config import settings
from datetime import datetime
import time
import logging
import asyncio

# NEW IMPORTS FOR FIX:
from sqlalchemy import create_engine
from .database import metadata, DATABASE_URL


app = FastAPI(title="Transaction Webhook Processor")

logger = logging.getLogger("uvicorn.error")

@app.on_event("startup")
async def startup():
    # ========== FIX FOR SQLITE + ASYNC ==========
    # Create tables using SYNC engine (SQLite requires this for DDL)
    sync_engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""), future=True)
    metadata.create_all(sync_engine)
    # now connect async DB
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {"status": "HEALTHY", "current_time": datetime.utcnow().isoformat() + "Z"}

@app.post("/v1/webhooks/transactions", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(payload: WebhookIn, background_tasks: BackgroundTasks, request: Request):
    """
    Receives webhook and schedules processing in background.
    Must respond quickly < 500ms (background tasks used).
    Returns 202 Accepted.
    """
    start = time.time()

    tx_payload = payload.dict()

    # Idempotency: create a PROCESSING record if not exists (returns existing if exists)
    tx = await create_processing(tx_payload)

    # If status already PROCESSED, do not queue processing again.
    if tx["status"] != "PROCESSED":
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(process_transaction_job(tx["transaction_id"]))
        except RuntimeError:
            background_tasks.add_task(process_transaction_job, tx["transaction_id"])

    elapsed = (time.time() - start) * 1000
    if elapsed > 500:
        logger.warning(f"Webhook handler took {elapsed:.2f}ms (should be <500ms)")

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"accepted": True, "transaction_id": tx["transaction_id"]}
    )

@app.get("/v1/transactions/{transaction_id}", response_model=TransactionOut)
async def get_transaction_status(transaction_id: str):
    tx = await get_transaction(transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {
        "transaction_id": tx["transaction_id"],
        "source_account": tx["source_account"],
        "destination_account": tx["destination_account"],
        "amount": float(tx["amount"]),
        "currency": tx["currency"],
        "status": tx["status"],
        "created_at": tx["created_at"],
        "processed_at": tx["processed_at"],
    }
