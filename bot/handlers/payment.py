"""Payment flow handlers."""
from datetime import datetime
from decimal import Decimal
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.models.user import User
from bot.models.order import Order, OrderRepository, OrderStatus, PaymentMethod
from bot.models.settings import SettingsRepository
from bot.utils.texts import get_text
from bot.utils.commission import calculate_commission, calculate_payment_amount
from bot.keyboards.inline import (
    get_payment_methods,
    get_payment_confirmation,
    get_active_order_menu,
    get_main_menu
)

router = Router()


class PaymentStates(StatesGroup):
    """Payment flow states."""
    waiting_for_service = State()
    waiting_for_amount = State()
    waiting_for_payment_method = State()
    waiting_for_confirmation = State()


@router.callback_query(F.data == "payment_start")
async def start_payment(
    callback: CallbackQuery,
    user: User,
    state: FSMContext,
    order_repo: OrderRepository
):
    """Start payment process."""
    # Check for active order
    active_order = await order_repo.get_active_order(user.telegram_id)

    if active_order:
        text = get_text(
            user.language,
            "active_order_exists",
            order_id=active_order.id
        )
        keyboard = get_active_order_menu(user.language, active_order.id)
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        return

    # Start payment flow
    text = get_text(user.language, "enter_service")
    await callback.message.edit_text(text)
    await state.set_state(PaymentStates.waiting_for_service)
    await callback.answer()


@router.message(PaymentStates.waiting_for_service)
async def process_service(message: Message, user: User, state: FSMContext):
    """Process service name input."""
    service_name = message.text.strip()

    # Save service name
    await state.update_data(service_name=service_name)

    # Ask for amount
    text = get_text(user.language, "enter_amount")
    await message.answer(text)
    await state.set_state(PaymentStates.waiting_for_amount)


@router.message(PaymentStates.waiting_for_amount)
async def process_amount(message: Message, user: User, state: FSMContext):
    """Process amount input."""
    try:
        amount = Decimal(message.text.strip())
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except (ValueError, Exception):
        text = get_text(user.language, "invalid_amount")
        await message.answer(text)
        return

    # Calculate commission
    commission_rate, commission_amount = calculate_commission(amount)
    total_amount = amount + commission_amount

    # Save data
    await state.update_data(
        base_amount=amount,
        commission_rate=commission_rate,
        commission_amount=commission_amount,
        total_amount=total_amount
    )

    # Show summary and payment methods
    text = get_text(
        user.language,
        "payment_summary",
        service=(await state.get_data())["service_name"],
        base_amount=float(amount),
        commission_rate=float(commission_rate),
        commission_amount=float(commission_amount),
        total_amount=float(total_amount)
    )
    keyboard = get_payment_methods(user.language)

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(PaymentStates.waiting_for_payment_method)


@router.callback_query(
    F.data.startswith("payment_method:"),
    PaymentStates.waiting_for_payment_method
)
async def process_payment_method(
    callback: CallbackQuery,
    user: User,
    state: FSMContext,
    order_repo: OrderRepository,
    settings_repo: SettingsRepository,
    bot: Bot,
    config
):
    """Process payment method selection."""
    payment_method = callback.data.split(":")[1]

    # Get state data
    data = await state.get_data()

    # Calculate payment amount
    total_amount = Decimal(str(data["total_amount"]))
    payment_amount, payment_currency = calculate_payment_amount(
        total_amount,
        payment_method,
        config.bot.usd_to_rub_rate
    )

    # Create order
    order = Order(
        user_id=user.telegram_id,
        service_name=data["service_name"],
        base_amount=Decimal(str(data["base_amount"])),
        commission_rate=Decimal(str(data["commission_rate"])),
        commission_amount=Decimal(str(data["commission_amount"])),
        total_amount=total_amount,
        payment_method=payment_method,
        payment_amount=payment_amount,
        payment_currency=payment_currency,
        status=OrderStatus.PENDING
    )

    order = await order_repo.create(order)

    # Get requisites
    requisites = await settings_repo.get_payment_requisites(payment_method)

    # Get payment method name
    method_name = get_text(user.language, f"method_{payment_method.lower()}")

    # Show payment details
    text = get_text(
        user.language,
        "payment_details",
        order_id=order.id,
        service=order.service_name,
        amount=f"{payment_amount:.2f}",
        currency=payment_currency,
        method=method_name,
        requisites=requisites or "Не указаны / Not specified"
    )
    keyboard = get_payment_confirmation(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.update_data(order_id=order.id)
    await state.set_state(PaymentStates.waiting_for_confirmation)

    # Notify admins about new order
    if config.bot.admin_chat_id:
        admin_text = get_text(
            "ru",
            "new_order_notification",
            id=order.id,
            user_id=user.telegram_id,
            service=order.service_name,
            amount=float(order.total_amount),
            method=method_name
        )
        try:
            await bot.send_message(
                config.bot.admin_chat_id,
                admin_text,
                parse_mode="HTML"
            )
        except Exception:
            pass

    await callback.answer()


@router.callback_query(F.data == "confirm_payment", PaymentStates.waiting_for_confirmation)
async def confirm_payment(
    callback: CallbackQuery,
    user: User,
    state: FSMContext,
    order_repo: OrderRepository,
    settings_repo: SettingsRepository,
    bot: Bot,
    config
):
    """Confirm payment from user."""
    data = await state.get_data()
    order_id = data.get("order_id")

    if not order_id:
        await callback.answer("Error: Order not found", show_alert=True)
        return

    # Get order
    order = await order_repo.get(order_id)
    if not order:
        await callback.answer("Error: Order not found", show_alert=True)
        return

    # Update order status
    await order_repo.update_status(
        order_id,
        OrderStatus.PAID_USER,
        paid_at=datetime.now()
    )

    # Get instruction
    instruction = await settings_repo.get_instruction(user.language)

    # Get payment method name
    method_name = get_text(user.language, f"method_{order.payment_method.lower()}")

    # Show receipt
    text = get_text(
        user.language,
        "payment_receipt",
        order_id=order.id,
        amount=f"{order.payment_amount:.2f}",
        currency=order.payment_currency,
        method=method_name,
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        instruction=instruction
    )

    keyboard = get_main_menu(user.language)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await state.clear()

    # Notify admins
    if config.bot.admin_chat_id:
        admin_text = get_text(
            "ru",
            "payment_notification",
            id=order.id,
            user_id=user.telegram_id,
            amount=f"{order.payment_amount:.2f}",
            currency=order.payment_currency,
            method=method_name,
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        try:
            from bot.keyboards.inline import get_order_admin_actions
            admin_keyboard = get_order_admin_actions("ru", order.id, OrderStatus.PAID_USER)
            await bot.send_message(
                config.bot.admin_chat_id,
                admin_text,
                reply_markup=admin_keyboard,
                parse_mode="HTML"
            )
        except Exception:
            pass

    await callback.answer()


@router.callback_query(F.data == "cancel_order")
async def cancel_order(
    callback: CallbackQuery,
    user: User,
    state: FSMContext,
    order_repo: OrderRepository
):
    """Cancel order."""
    data = await state.get_data()
    order_id = data.get("order_id")

    if order_id:
        await order_repo.update_status(order_id, OrderStatus.REJECTED)

    text = get_text(user.language, "order_cancelled", order_id=order_id or "N/A")
    keyboard = get_main_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await state.clear()
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_order:"))
async def cancel_order_by_id(
    callback: CallbackQuery,
    user: User,
    order_repo: OrderRepository
):
    """Cancel order by ID."""
    order_id = int(callback.data.split(":")[1])

    await order_repo.update_status(order_id, OrderStatus.REJECTED)

    text = get_text(user.language, "order_cancelled", order_id=order_id)
    keyboard = get_main_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("view_order:"))
async def view_order(
    callback: CallbackQuery,
    user: User,
    order_repo: OrderRepository
):
    """View order details."""
    order_id = int(callback.data.split(":")[1])

    order = await order_repo.get(order_id)
    if not order:
        await callback.answer("Order not found", show_alert=True)
        return

    method_name = get_text(user.language, f"method_{order.payment_method.lower()}")
    status_name = get_text(user.language, f"status_{order.status.lower()}")

    text = get_text(
        user.language,
        "order_details",
        id=order.id,
        service=order.service_name,
        base_amount=float(order.base_amount),
        commission=float(order.commission_amount),
        total=float(order.total_amount),
        method=method_name,
        status=status_name,
        created_at=order.created_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    from bot.keyboards.inline import get_order_details_menu
    keyboard = get_order_details_menu(user.language)

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
