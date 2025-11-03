from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./transactions.db"
    webhook_secret: str | None = None
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = "../.env"

settings = Settings()
