# crud.py
from .database import database, transactions
from sqlalchemy import select, insert, update
from datetime import datetime
from typing import Optional
from decimal import Decimal

async def get_transaction(transaction_id: str) -> Optional[dict]:
    query = select(transactions).where(transactions.c.transaction_id == transaction_id)
    row = await database.fetch_one(query)
    if row:
        return dict(row)
    return None

async def create_processing(transaction_data: dict) -> dict:
    # Insert a row with status PROCESSING only if transaction_id not exists
    existing = await get_transaction(transaction_data["transaction_id"])
    if existing:
        return existing
    query = insert(transactions).values(
        transaction_id=transaction_data["transaction_id"],
        source_account=transaction_data["source_account"],
        destination_account=transaction_data["destination_account"],
        amount=Decimal(str(transaction_data["amount"])),
        currency=transaction_data["currency"],
        status="PROCESSING",
    )
    await database.execute(query)
    return await get_transaction(transaction_data["transaction_id"])

async def mark_processed(transaction_id: str, success: bool = True):
    now = datetime.utcnow()
    status = "PROCESSED" if success else "FAILED"
    query = update(transactions).where(transactions.c.transaction_id == transaction_id).values(
        status=status,
        processed_at=now
    )
    await database.execute(query)
    return await get_transaction(transaction_id)
