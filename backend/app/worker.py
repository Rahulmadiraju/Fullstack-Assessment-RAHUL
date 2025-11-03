# worker.py
import asyncio
import logging
from .crud import mark_processed, get_transaction
from datetime import datetime

logger = logging.getLogger("worker")
logger.setLevel(logging.INFO)

async def process_transaction_job(transaction_id: str):
    """
    Simulates an external API call / processing that takes 30 seconds.
    Marks the transaction PROCESSED when done.
    Idempotency: if already PROCESSED, skip.
    """
    try:
        logger.info(f"Worker: starting processing for {transaction_id}")
        tx = await get_transaction(transaction_id)
        if not tx:
            logger.warning(f"Worker: tx {transaction_id} not found; skipping.")
            return
        if tx["status"] == "PROCESSED":
            logger.info(f"Worker: tx {transaction_id} already processed; skipping.")
            return
        # Simulate long-running processing
        await asyncio.sleep(30)  # <-- required 30 second simulated delay
        # In real life: call external APIs, handle errors, compensation etc.
        await mark_processed(transaction_id, success=True)
        logger.info(f"Worker: finished processing for {transaction_id}")
    except Exception as e:
        logger.exception("Worker: error during processing")
        # Attempt to mark as failed
        try:
            await mark_processed(transaction_id, success=False)
        except Exception:
            pass
