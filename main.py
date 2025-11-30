"""Main bot entry point."""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import load_config
from bot.database.db import Database
from bot.models.user import UserRepository
from bot.models.order import OrderRepository
from bot.models.settings import SettingsRepository
from bot.middlewares.user_check import UserCheckMiddleware
from bot.filters.admin import AdminFilter

# Import handlers
from bot.handlers import common, payment, profile, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot function."""
    # Load configuration
    config = load_config()

    # Initialize bot and dispatcher
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Initialize database
    db = Database(config.db.dsn)
    await db.connect()

    # Initialize repositories
    user_repo = UserRepository(db)
    order_repo = OrderRepository(db)
    settings_repo = SettingsRepository(db)

    # Initialize admin filter
    admin_filter = AdminFilter(config.bot.admin_ids)

    # Register middlewares
    common.router.message.middleware(UserCheckMiddleware(user_repo))
    common.router.callback_query.middleware(UserCheckMiddleware(user_repo))
    payment.router.message.middleware(UserCheckMiddleware(user_repo))
    payment.router.callback_query.middleware(UserCheckMiddleware(user_repo))
    profile.router.callback_query.middleware(UserCheckMiddleware(user_repo))
    admin.router.message.middleware(UserCheckMiddleware(user_repo))
    admin.router.callback_query.middleware(UserCheckMiddleware(user_repo))

    # Register routers
    dp.include_router(common.router)
    dp.include_router(payment.router)
    dp.include_router(profile.router)
    dp.include_router(admin.router)

    # Set data to all handlers
    dp.workflow_data.update({
        "config": config,
        "db": db,
        "user_repo": user_repo,
        "order_repo": order_repo,
        "settings_repo": settings_repo,
        "admin_filter": admin_filter
    })

    # Start polling
    try:
        logger.info("Bot started")
        await dp.start_polling(bot)
    finally:
        await db.disconnect()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
