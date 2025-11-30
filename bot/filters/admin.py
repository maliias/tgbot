"""Admin filter."""
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from typing import Union


class AdminFilter(BaseFilter):
    """Filter to check if user is admin."""

    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        """Check if user is admin."""
        user_id = event.from_user.id
        return user_id in self.admin_ids
