from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    kalshi_base_url: str = "https://external-api.kalshi.com/trade-api/v2"
    scan_interval_seconds: int = 60
    market_limit: int = 200
    min_volume: float = 0
    fee_safety_buffer_cents: int = 3
    db_path: str = "./data/kalshi_shadow.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
