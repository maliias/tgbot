"""Inline keyboard layouts."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.utils.texts import get_text


def get_main_menu(language: str) -> InlineKeyboardMarkup:
    """Get main menu keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_payment"),
            callback_data="payment_start"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_profile"),
            callback_data="profile"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_info"),
            callback_data="info"
        ),
        InlineKeyboardButton(
            text=get_text(language, "btn_language"),
            callback_data="language"
        )
    )

    return builder.as_markup()


def get_payment_methods(language: str) -> InlineKeyboardMarkup:
    """Get payment methods keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_usdt_trc20"),
            callback_data="payment_method:USDT_TRC20"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_usdt_bep20"),
            callback_data="payment_method:USDT_BEP20"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_bybit"),
            callback_data="payment_method:BYBIT_UID"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_card"),
            callback_data="payment_method:CARD"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_lolz"),
            callback_data="payment_method:LOLZ"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="main_menu"
        )
    )

    return builder.as_markup()


def get_payment_confirmation(language: str) -> InlineKeyboardMarkup:
    """Get payment confirmation keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_paid"),
            callback_data="confirm_payment"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_cancel_order"),
            callback_data="cancel_order"
        )
    )

    return builder.as_markup()


def get_active_order_menu(language: str, order_id: int) -> InlineKeyboardMarkup:
    """Get active order menu keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_view_order"),
            callback_data=f"view_order:{order_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_cancel_current"),
            callback_data=f"cancel_order:{order_id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="main_menu"
        )
    )

    return builder.as_markup()


def get_profile_menu(language: str) -> InlineKeyboardMarkup:
    """Get profile menu keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_my_orders"),
            callback_data="my_orders"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="main_menu"
        )
    )

    return builder.as_markup()


def get_orders_list(language: str, orders: list, page: int = 0) -> InlineKeyboardMarkup:
    """Get orders list keyboard."""
    builder = InlineKeyboardBuilder()

    # Add order buttons
    for order in orders:
        status_text = get_text(language, f"status_{order.status.lower()}")
        button_text = f"#{order.id} - {order.service_name[:20]} - {status_text}"
        builder.row(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"view_order:{order.id}"
            )
        )

    # Back button
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="profile"
        )
    )

    return builder.as_markup()


def get_order_details_menu(language: str) -> InlineKeyboardMarkup:
    """Get order details menu keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="my_orders"
        )
    )

    return builder.as_markup()


def get_language_menu() -> InlineKeyboardMarkup:
    """Get language selection keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="🇷🇺 Русский",
            callback_data="set_language:ru"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="🇬🇧 English",
            callback_data="set_language:en"
        )
    )

    return builder.as_markup()


def get_info_menu(language: str, settings: dict) -> InlineKeyboardMarkup:
    """Get info menu keyboard with links from settings."""
    builder = InlineKeyboardBuilder()

    # Add buttons with URLs from settings
    if settings.get("info_channel_url"):
        builder.row(
            InlineKeyboardButton(
                text=get_text(language, "btn_channel"),
                url=settings["info_channel_url"]
            )
        )

    if settings.get("info_support_url"):
        builder.row(
            InlineKeyboardButton(
                text=get_text(language, "btn_support"),
                url=settings["info_support_url"]
            )
        )

    if settings.get("info_terms_url"):
        builder.row(
            InlineKeyboardButton(
                text=get_text(language, "btn_terms"),
                url=settings["info_terms_url"]
            )
        )

    if settings.get("info_refund_url"):
        builder.row(
            InlineKeyboardButton(
                text=get_text(language, "btn_refund"),
                url=settings["info_refund_url"]
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="main_menu"
        )
    )

    return builder.as_markup()


# Admin keyboards
def get_admin_menu(language: str) -> InlineKeyboardMarkup:
    """Get admin panel keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_stats"),
            callback_data="admin_stats"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_orders"),
            callback_data="admin_orders"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_settings"),
            callback_data="admin_settings"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_broadcast"),
            callback_data="admin_broadcast"
        )
    )

    return builder.as_markup()


def get_stats_period_menu(language: str) -> InlineKeyboardMarkup:
    """Get statistics period selection keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_stats_day"),
            callback_data="stats_period:day"
        ),
        InlineKeyboardButton(
            text=get_text(language, "btn_stats_week"),
            callback_data="stats_period:week"
        ),
        InlineKeyboardButton(
            text=get_text(language, "btn_stats_month"),
            callback_data="stats_period:month"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="admin_panel"
        )
    )

    return builder.as_markup()


def get_orders_filter_menu(language: str) -> InlineKeyboardMarkup:
    """Get orders filter keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_filter_all"),
            callback_data="admin_orders_filter:all"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_filter_pending"),
            callback_data="admin_orders_filter:PENDING"
        ),
        InlineKeyboardButton(
            text=get_text(language, "btn_filter_paid"),
            callback_data="admin_orders_filter:PAID_USER"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_filter_completed"),
            callback_data="admin_orders_filter:COMPLETED"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="admin_panel"
        )
    )

    return builder.as_markup()


def get_admin_orders_list(language: str, orders: list) -> InlineKeyboardMarkup:
    """Get admin orders list keyboard."""
    builder = InlineKeyboardBuilder()

    for order in orders[:10]:  # Limit to 10 orders per page
        status_text = get_text(language, f"status_{order.status.lower()}")
        button_text = f"#{order.id} - ${order.total_amount:.2f} - {status_text}"
        builder.row(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"admin_order:{order.id}"
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="admin_orders"
        )
    )

    return builder.as_markup()


def get_order_admin_actions(language: str, order_id: int, current_status: str) -> InlineKeyboardMarkup:
    """Get order admin actions keyboard."""
    builder = InlineKeyboardBuilder()

    if current_status != "COMPLETED":
        builder.row(
            InlineKeyboardButton(
                text=get_text(language, "btn_complete"),
                callback_data=f"admin_order_status:{order_id}:COMPLETED"
            )
        )

    if current_status not in ["REJECTED", "COMPLETED"]:
        builder.row(
            InlineKeyboardButton(
                text=get_text(language, "btn_reject"),
                callback_data=f"admin_order_status:{order_id}:REJECTED"
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="admin_orders_filter:all"
        )
    )

    return builder.as_markup()


def get_broadcast_confirm(language: str) -> InlineKeyboardMarkup:
    """Get broadcast confirmation keyboard."""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_confirm"),
            callback_data="broadcast_confirm"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=get_text(language, "btn_back"),
            callback_data="admin_panel"
        )
    )

    return builder.as_markup()
