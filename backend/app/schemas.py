from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WebhookIn(BaseModel):
    transaction_id: str = Field(..., example="txn_abc123def456")
    source_account: str = Field(..., example="acc_user_789")
    destination_account: str = Field(..., example="acc_merchant_456")
    amount: float = Field(..., example=1500)
    currency: str = Field(..., example="INR")

class TransactionOut(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
