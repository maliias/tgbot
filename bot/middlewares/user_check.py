"""Middleware to check user status."""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from bot.models.user import UserRepository
from bot.utils.texts import get_text


class UserCheckMiddleware(BaseMiddleware):
    """Middleware to check if user is blocked."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Check user status before handling."""
        user_id = event.from_user.id

        # Get or create user
        user = await self.user_repo.get_or_create(
            telegram_id=user_id,
            username=event.from_user.username,
            first_name=event.from_user.first_name
        )

        # Check if user is blocked
        if user.is_blocked:
            if isinstance(event, Message):
                await event.answer(get_text(user.language, "user_blocked"))
            elif isinstance(event, CallbackQuery):
                await event.answer(get_text(user.language, "user_blocked"), show_alert=True)
            return

        # Add user to data
        data["user"] = user

        return await handler(event, data)
