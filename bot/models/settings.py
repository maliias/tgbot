"""Settings model and database operations."""
from typing import Optional


class SettingsRepository:
    """Settings database operations."""

    def __init__(self, db):
        self.db = db

    async def get(self, key: str) -> Optional[str]:
        """Get setting value by key."""
        query = "SELECT value FROM settings WHERE key = $1"
        return await self.db.fetchval(query, key)

    async def set(self, key: str, value: str):
        """Set setting value."""
        query = """
            INSERT INTO settings (key, value)
            VALUES ($1, $2)
            ON CONFLICT (key) DO UPDATE
            SET value = EXCLUDED.value
        """
        await self.db.execute(query, key, value)

    async def get_payment_requisites(self, payment_method: str) -> str:
        """Get payment requisites by method."""
        method_map = {
            "USDT_TRC20": "usdt_trc20_address",
            "USDT_BEP20": "usdt_bep20_address",
            "BYBIT_UID": "bybit_uid",
            "CARD": "card_number",
            "LOLZ": "lolz_requisites"
        }
        key = method_map.get(payment_method)
        if key:
            return await self.get(key) or ""
        return ""

    async def get_instruction(self, language: str) -> str:
        """Get instruction text by language."""
        key = f"instruction_text_{language}"
        return await self.get(key) or ""

    async def set_instruction(self, language: str, text: str):
        """Set instruction text."""
        key = f"instruction_text_{language}"
        await self.set(key, text)

    async def get_all_settings(self) -> dict:
        """Get all settings."""
        query = "SELECT key, value FROM settings"
        records = await self.db.fetch(query)
        return {record["key"]: record["value"] for record in records}
