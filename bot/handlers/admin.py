"""Admin panel handlers."""
from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.models.user import User, UserRepository
from bot.models.order import OrderRepository, OrderStatus
from bot.filters.admin import AdminFilter
from bot.utils.texts import get_text
from bot.keyboards.inline import (
    get_admin_menu,
    get_stats_period_menu,
    get_orders_filter_menu,
    get_admin_orders_list,
    get_order_admin_actions,
    get_broadcast_confirm,
    get_main_menu
)

router = Router()


class AdminStates(StatesGroup):
    """Admin states."""
    waiting_for_broadcast = State()


@router.message(Command("admin"))
async def cmd_admin(message: Message, user: User, admin_filter: AdminFilter):
    """Show admin panel."""
    if not await admin_filter(message):
        return

    text = get_text(user.language, "admin_panel")
    keyboard = get_admin_menu(user.language)

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "admin_panel")
async def show_admin_panel(callback: CallbackQuery, user: User, state: FSMContext):
    """Show admin panel."""
    await state.clear()

    text = get_text(user.language, "admin_panel")
    keyboard = get_admin_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def show_stats_menu(callback: CallbackQuery, user: User):
    """Show statistics menu."""
    text = get_text(user.language, "stats_period")
    keyboard = get_stats_period_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("stats_period:"))
async def show_stats(callback: CallbackQuery, user: User, order_repo: OrderRepository):
    """Show statistics for period."""
    period = callback.data.split(":")[1]

    # Calculate date range
    end_date = datetime.now()
    if period == "day":
        start_date = end_date - timedelta(days=1)
    elif period == "week":
        start_date = end_date - timedelta(weeks=1)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    else:
        start_date = end_date - timedelta(days=1)

    # Get stats
    stats = await order_repo.get_stats(start_date, end_date)

    text = get_text(
        user.language,
        "stats_message",
        total_orders=stats["total_orders"],
        completed_orders=stats["completed_orders"],
        success_rate=stats["success_rate"],
        total_turnover_usd=stats["total_turnover_usd"],
        total_turnover_rub=stats["total_turnover_rub"],
        total_commission=stats["total_commission"]
    )

    keyboard = get_stats_period_menu(user.language)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin_orders")
async def show_orders_filter(callback: CallbackQuery, user: User):
    """Show orders filter menu."""
    text = get_text(user.language, "orders_list")
    keyboard = get_orders_filter_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("admin_orders_filter:"))
async def show_orders_list(callback: CallbackQuery, user: User, order_repo: OrderRepository):
    """Show orders list with filter."""
    filter_type = callback.data.split(":")[1]

    # Get orders
    if filter_type == "all":
        orders = await order_repo.get_all_orders(limit=10)
    else:
        orders = await order_repo.get_all_orders(status=filter_type, limit=10)

    if not orders:
        text = get_text(user.language, "no_orders")
        keyboard = get_orders_filter_menu(user.language)
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        return

    text = get_text(user.language, "orders_list")
    keyboard = get_admin_orders_list(user.language, orders)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_order:"))
async def show_order_details(callback: CallbackQuery, user: User, order_repo: OrderRepository):
    """Show order details for admin."""
    order_id = int(callback.data.split(":")[1])

    order = await order_repo.get(order_id)
    if not order:
        await callback.answer("Order not found", show_alert=True)
        return

    method_name = get_text(user.language, f"method_{order.payment_method.lower()}")
    status_name = get_text(user.language, f"status_{order.status.lower()}")

    text = get_text(
        user.language,
        "order_admin_details",
        id=order.id,
        user_id=order.user_id,
        service=order.service_name,
        total=float(order.total_amount),
        method=method_name,
        status=status_name,
        created_at=order.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    keyboard = get_order_admin_actions(user.language, order.id, order.status)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_order_status:"))
async def update_order_status(
    callback: CallbackQuery,
    user: User,
    order_repo: OrderRepository,
    bot: Bot
):
    """Update order status."""
    parts = callback.data.split(":")
    order_id = int(parts[1])
    new_status = parts[2]

    # Update status
    completed_at = datetime.now() if new_status == OrderStatus.COMPLETED else None
    await order_repo.update_status(order_id, new_status, completed_at=completed_at)

    # Get updated order
    order = await order_repo.get(order_id)

    # Notify user about status change
    try:
        from bot.models.user import UserRepository
        user_repo = UserRepository(order_repo.db)
        order_user = await user_repo.get(order.user_id)

        if order_user:
            if new_status == OrderStatus.COMPLETED:
                notification = f"✅ Ваш заказ #{order_id} успешно выполнен!"
            else:
                notification = f"❌ Ваш заказ #{order_id} был отклонен."

            keyboard = get_main_menu(order_user.language)
            await bot.send_message(
                order.user_id,
                notification,
                reply_markup=keyboard
            )
    except Exception:
        pass

    # Show updated order details
    method_name = get_text(user.language, f"method_{order.payment_method.lower()}")
    status_name = get_text(user.language, f"status_{order.status.lower()}")

    text = get_text(
        user.language,
        "order_admin_details",
        id=order.id,
        user_id=order.user_id,
        service=order.service_name,
        total=float(order.total_amount),
        method=method_name,
        status=status_name,
        created_at=order.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    keyboard = get_order_admin_actions(user.language, order.id, order.status)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer(get_text(user.language, "order_status_updated"))


@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: CallbackQuery, user: User, state: FSMContext):
    """Start broadcast."""
    text = get_text(user.language, "broadcast_enter_text")
    await callback.message.edit_text(text)
    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.answer()


@router.message(AdminStates.waiting_for_broadcast)
async def process_broadcast_text(message: Message, user: User, state: FSMContext):
    """Process broadcast text."""
    broadcast_text = message.text

    await state.update_data(broadcast_text=broadcast_text)

    text = get_text(
        user.language,
        "broadcast_confirm",
        text=broadcast_text
    )
    keyboard = get_broadcast_confirm(user.language)

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "broadcast_confirm", AdminStates.waiting_for_broadcast)
async def confirm_broadcast(
    callback: CallbackQuery,
    user: User,
    state: FSMContext,
    user_repo: UserRepository,
    bot: Bot
):
    """Confirm and send broadcast."""
    data = await state.get_data()
    broadcast_text = data.get("broadcast_text")

    if not broadcast_text:
        await callback.answer("Error: No text", show_alert=True)
        return

    # Get all users
    users = await user_repo.get_all_users()

    # Send broadcast
    sent_count = 0
    for target_user in users:
        if not target_user.is_blocked:
            try:
                await bot.send_message(target_user.telegram_id, broadcast_text)
                sent_count += 1
            except Exception:
                pass

    text = get_text(user.language, "broadcast_sent", count=sent_count)
    await callback.message.edit_text(text)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "admin_settings")
async def show_settings(callback: CallbackQuery, user: User):
    """Show settings menu (placeholder)."""
    text = "⚙️ <b>Настройки</b>\n\nДля изменения настроек используйте команды базы данных или файл .env"
    keyboard = get_admin_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
