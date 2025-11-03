# database.py
from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.sql import func
from .config import settings

DATABASE_URL = settings.database_url

# Use databases library for async interactions
database = Database(DATABASE_URL)
metadata = MetaData()

transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("transaction_id", String, unique=True, nullable=False),
    Column("source_account", String, nullable=False),
    Column("destination_account", String, nullable=False),
    Column("amount", Numeric, nullable=False),
    Column("currency", String, nullable=False),
    Column("status", String, nullable=False),  # PROCESSING, PROCESSED, FAILED
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("processed_at", DateTime(timezone=True), nullable=True),
)

# create synchronous engine for metadata.create_all
engine = create_engine(DATABASE_URL, future=True)

