"""Configuration module for the payment bot."""
import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    """Database configuration."""
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def dsn(self) -> str:
        """Get database connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class BotConfig:
    """Bot configuration."""
    token: str
    admin_ids: List[int]
    admin_chat_id: int
    usd_to_rub_rate: float


@dataclass
class Config:
    """Main configuration class."""
    bot: BotConfig
    db: DatabaseConfig


def load_config() -> Config:
    """Load configuration from environment variables."""
    return Config(
        bot=BotConfig(
            token=os.getenv("BOT_TOKEN"),
            admin_ids=[int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x],
            admin_chat_id=int(os.getenv("ADMIN_CHAT_ID", "0")),
            usd_to_rub_rate=float(os.getenv("USD_TO_RUB_RATE", "95.50"))
        ),
        db=DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "payment_bot"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )
    )
