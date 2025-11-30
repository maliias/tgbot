"""User model and database operations."""
from datetime import datetime
from typing import Optional, Dict, Any
import asyncpg


class User:
    """User model."""

    def __init__(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        language: str = "ru",
        is_blocked: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.language = language
        self.is_blocked = is_blocked
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "User":
        """Create User instance from database record."""
        return cls(
            telegram_id=record["telegram_id"],
            username=record["username"],
            first_name=record["first_name"],
            language=record["language"],
            is_blocked=record["is_blocked"],
            created_at=record["created_at"],
            updated_at=record["updated_at"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "language": self.language,
            "is_blocked": self.is_blocked,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class UserRepository:
    """User database operations."""

    def __init__(self, db):
        self.db = db

    async def get_or_create(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None
    ) -> User:
        """Get existing user or create new one."""
        query = """
            INSERT INTO users (telegram_id, username, first_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id) DO UPDATE
            SET username = EXCLUDED.username,
                first_name = EXCLUDED.first_name
            RETURNING *
        """
        record = await self.db.fetchrow(query, telegram_id, username, first_name)
        return User.from_record(record)

    async def get(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram_id."""
        query = "SELECT * FROM users WHERE telegram_id = $1"
        record = await self.db.fetchrow(query, telegram_id)
        return User.from_record(record) if record else None

    async def update_language(self, telegram_id: int, language: str):
        """Update user language."""
        query = "UPDATE users SET language = $1 WHERE telegram_id = $2"
        await self.db.execute(query, language, telegram_id)

    async def block_user(self, telegram_id: int):
        """Block user."""
        query = "UPDATE users SET is_blocked = TRUE WHERE telegram_id = $1"
        await self.db.execute(query, telegram_id)

    async def unblock_user(self, telegram_id: int):
        """Unblock user."""
        query = "UPDATE users SET is_blocked = FALSE WHERE telegram_id = $1"
        await self.db.execute(query, telegram_id)

    async def get_all_users(self) -> list[User]:
        """Get all users."""
        query = "SELECT * FROM users ORDER BY created_at DESC"
        records = await self.db.fetch(query)
        return [User.from_record(record) for record in records]

    async def count_all_users(self) -> int:
        """Count all users."""
        query = "SELECT COUNT(*) FROM users"
        return await self.db.fetchval(query)
