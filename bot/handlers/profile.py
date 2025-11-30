"""User profile and orders handlers."""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.models.user import User
from bot.models.order import OrderRepository
from bot.utils.texts import get_text
from bot.keyboards.inline import get_profile_menu, get_orders_list, get_order_details_menu

router = Router()


@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery, user: User, order_repo: OrderRepository, state: FSMContext):
    """Show user profile."""
    await state.clear()

    # Get user stats
    stats = await order_repo.get_user_stats(user.telegram_id)

    # Format dates
    first_payment = stats["first_payment"].strftime("%Y-%m-%d") if stats["first_payment"] else "N/A"
    last_payment = stats["last_payment"].strftime("%Y-%m-%d") if stats["last_payment"] else "N/A"

    text = get_text(
        user.language,
        "profile",
        telegram_id=user.telegram_id,
        user_language=user.language.upper(),
        completed_count=stats["completed_count"],
        total_spent=stats["total_spent"],
        first_payment=first_payment,
        last_payment=last_payment
    )

    keyboard = get_profile_menu(user.language)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "my_orders")
async def show_my_orders(callback: CallbackQuery, user: User, order_repo: OrderRepository):
    """Show user orders."""
    orders = await order_repo.get_user_orders(user.telegram_id, limit=10)

    if not orders:
        text = get_text(user.language, "no_orders")
        keyboard = get_profile_menu(user.language)
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        return

    text = get_text(user.language, "my_orders")
    keyboard = get_orders_list(user.language, orders)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
