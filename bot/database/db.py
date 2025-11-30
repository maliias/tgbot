"""Database connection and query execution."""
import asyncpg
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Create database connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                self.dsn,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            logger.info("Database connection pool created")

            # Initialize database schema
            await self.init_schema()
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self):
        """Close database connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    async def init_schema(self):
        """Initialize database schema."""
        try:
            with open("bot/database/schema.sql", "r", encoding="utf-8") as f:
                schema = f.read()

            async with self.pool.acquire() as conn:
                await conn.execute(schema)

            logger.info("Database schema initialized")
        except Exception as e:
            logger.error(f"Failed to initialize schema: {e}")
            raise

    async def execute(self, query: str, *args) -> str:
        """Execute a query without returning results."""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> List[asyncpg.Record]:
        """Fetch multiple rows."""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Fetch a single row."""
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args) -> Any:
        """Fetch a single value."""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)
