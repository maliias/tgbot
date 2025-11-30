"""Multilingual text messages for the bot."""

TEXTS = {
    "ru": {
        # Main menu
        "main_menu": "🏠 Главное меню",
        "btn_payment": "💳 Оплата зарубежных сервисов",
        "btn_profile": "👤 Мой профиль",
        "btn_info": "ℹ️ Информация",
        "btn_language": "🌐 Язык / Language",

        # Payment flow
        "enter_service": "📝 Введите домен или название сервиса, который нужно оплатить:",
        "enter_amount": "💵 Введите сумму в USD:",
        "invalid_amount": "❌ Некорректная сумма. Пожалуйста, введите число больше 0.",
        "payment_summary": (
            "📊 <b>Детали заказа:</b>\n\n"
            "🔹 Сервис: <code>{service}</code>\n"
            "🔹 Базовая сумма: <code>${base_amount:.2f}</code>\n"
            "🔹 Комиссия ({commission_rate}%): <code>${commission_amount:.2f}</code>\n"
            "🔹 <b>Итого к оплате: ${total_amount:.2f}</b>\n\n"
            "Выберите способ оплаты:"
        ),
        "btn_usdt_trc20": "💰 USDT (TRC-20)",
        "btn_usdt_bep20": "💰 USDT (BEP-20)",
        "btn_bybit": "🟡 Bybit UID",
        "btn_card": "💳 Перевод по карте",
        "btn_lolz": "🧩 Lolz",

        # Payment details
        "payment_details": (
            "💳 <b>Заказ #{order_id}</b>\n\n"
            "🔹 Сервис: <code>{service}</code>\n"
            "🔹 Сумма к оплате: <b>{amount} {currency}</b>\n"
            "🔹 Способ оплаты: <b>{method}</b>\n\n"
            "📋 <b>Реквизиты для оплаты:</b>\n"
            "<code>{requisites}</code>\n\n"
            "После оплаты нажмите кнопку ниже:"
        ),
        "btn_paid": "✅ Я оплатил",
        "btn_cancel_order": "❌ Отменить заказ",

        # Payment receipt
        "payment_receipt": (
            "✅ <b>Оплата принята!</b>\n\n"
            "🧾 <b>Чек заказа #{order_id}</b>\n"
            "🔹 Сумма: <code>{amount} {currency}</code>\n"
            "🔹 Способ оплаты: <code>{method}</code>\n"
            "🔹 Дата и время: <code>{datetime}</code>\n\n"
            "📝 <b>Инструкция:</b>\n{instruction}\n\n"
            "⏳ Ваш заказ обрабатывается. Ожидайте подтверждения от администратора."
        ),

        # Order management
        "order_cancelled": "❌ Заказ #{order_id} отменен.",
        "active_order_exists": (
            "⚠️ У вас уже есть активный заказ #{order_id}.\n\n"
            "Пожалуйста, завершите текущий заказ перед созданием нового."
        ),
        "btn_view_order": "👀 Посмотреть заказ",
        "btn_cancel_current": "❌ Отменить заказ",

        # Profile
        "profile": (
            "👤 <b>Мой профиль</b>\n\n"
            "🆔 Telegram ID: <code>{telegram_id}</code>\n"
            "🌐 Язык: <code>{language}</code>\n"
            "✅ Успешных заказов: <code>{completed_count}</code>\n"
            "💰 Общая сумма: <code>${total_spent:.2f}</code>\n"
            "📅 Первая оплата: <code>{first_payment}</code>\n"
            "📅 Последняя оплата: <code>{last_payment}</code>"
        ),
        "btn_my_orders": "📦 Мои заказы",
        "btn_back": "◀️ Назад",

        # Orders list
        "my_orders": "📦 <b>Мои заказы:</b>",
        "no_orders": "У вас пока нет заказов.",
        "order_item": "#{id} - {service} - ${amount:.2f} - {status}",

        # Order details
        "order_details": (
            "📋 <b>Заказ #{id}</b>\n\n"
            "🔹 Сервис: <code>{service}</code>\n"
            "🔹 Базовая сумма: <code>${base_amount:.2f}</code>\n"
            "🔹 Комиссия: <code>${commission:.2f}</code>\n"
            "🔹 Итого: <code>${total:.2f}</code>\n"
            "🔹 Способ оплаты: <code>{method}</code>\n"
            "🔹 Статус: <code>{status}</code>\n"
            "🔹 Создан: <code>{created_at}</code>"
        ),

        # Info
        "info_message": "ℹ️ <b>Информация</b>\n\nВыберите интересующий раздел:",
        "btn_channel": "📢 Наш канал",
        "btn_support": "💬 Поддержка",
        "btn_terms": "📄 Пользовательское соглашение",
        "btn_refund": "💸 Политика возврата",

        # Language selection
        "select_language": "🌐 Выберите язык / Select language:",
        "language_changed": "✅ Язык изменен на Русский",

        # Status names
        "status_pending": "Ожидает оплаты",
        "status_paid_user": "Оплачен, требует проверки",
        "status_completed": "Успешно выполнен",
        "status_rejected": "Отменен",

        # Payment methods
        "method_usdt_trc20": "USDT (TRC-20)",
        "method_usdt_bep20": "USDT (BEP-20)",
        "method_bybit_uid": "Bybit UID",
        "method_card": "Перевод по карте",
        "method_lolz": "Lolz",

        # Errors
        "user_blocked": "🚫 Ваш доступ к боту ограничен. Обратитесь в поддержку.",
        "error_occurred": "❌ Произошла ошибка. Попробуйте позже.",

        # Admin
        "admin_panel": "🔧 <b>Панель администратора</b>",
        "btn_stats": "📊 Статистика",
        "btn_orders": "📋 Заказы",
        "btn_users": "👥 Пользователи",
        "btn_settings": "⚙️ Настройки",
        "btn_broadcast": "📢 Рассылка",

        "stats_period": "📊 Статистика за период:",
        "btn_stats_day": "День",
        "btn_stats_week": "Неделя",
        "btn_stats_month": "Месяц",

        "stats_message": (
            "📊 <b>Статистика</b>\n\n"
            "🔹 Всего заказов: <code>{total_orders}</code>\n"
            "🔹 Успешных: <code>{completed_orders}</code>\n"
            "🔹 Процент успеха: <code>{success_rate}%</code>\n"
            "🔹 Оборот (USD): <code>${total_turnover_usd:.2f}</code>\n"
            "🔹 Оборот (RUB): <code>₽{total_turnover_rub:.2f}</code>\n"
            "🔹 Комиссия: <code>${total_commission:.2f}</code>"
        ),

        "orders_list": "📋 <b>Заказы:</b>",
        "btn_filter_all": "Все",
        "btn_filter_pending": "Ожидают",
        "btn_filter_paid": "Оплачены",
        "btn_filter_completed": "Выполнены",

        "order_admin_details": (
            "📋 <b>Заказ #{id}</b>\n\n"
            "👤 Пользователь: {user_id}\n"
            "🔹 Сервис: {service}\n"
            "🔹 Сумма: ${total:.2f}\n"
            "🔹 Способ: {method}\n"
            "🔹 Статус: {status}\n"
            "🔹 Создан: {created_at}\n\n"
            "Изменить статус:"
        ),

        "btn_complete": "✅ Выполнен",
        "btn_reject": "❌ Отклонить",
        "order_status_updated": "✅ Статус заказа обновлен",

        # Broadcast
        "broadcast_enter_text": "📢 Введите текст рассылки:",
        "broadcast_confirm": (
            "📢 <b>Рассылка</b>\n\n"
            "Текст:\n{text}\n\n"
            "Отправить сообщение всем пользователям?"
        ),
        "btn_confirm": "✅ Подтвердить",
        "broadcast_sent": "✅ Рассылка отправлена {count} пользователям",

        # Notifications
        "new_order_notification": (
            "🔔 <b>Новый заказ #{id}</b>\n\n"
            "👤 Пользователь: {user_id}\n"
            "🔹 Сервис: {service}\n"
            "🔹 Сумма: ${amount:.2f}\n"
            "🔹 Способ: {method}"
        ),

        "payment_notification": (
            "💰 <b>Оплата по заказу #{id}</b>\n\n"
            "👤 Пользователь: {user_id}\n"
            "🔹 Сумма: {amount} {currency}\n"
            "🔹 Способ: {method}\n"
            "🔹 Время: {datetime}\n\n"
            "⚠️ Требует проверки!"
        ),
    },

    "en": {
        # Main menu
        "main_menu": "🏠 Main menu",
        "btn_payment": "💳 Pay for foreign services",
        "btn_profile": "👤 My profile",
        "btn_info": "ℹ️ Information",
        "btn_language": "🌐 Language / Язык",

        # Payment flow
        "enter_service": "📝 Enter the domain or name of the service to pay for:",
        "enter_amount": "💵 Enter amount in USD:",
        "invalid_amount": "❌ Invalid amount. Please enter a number greater than 0.",
        "payment_summary": (
            "📊 <b>Order details:</b>\n\n"
            "🔹 Service: <code>{service}</code>\n"
            "🔹 Base amount: <code>${base_amount:.2f}</code>\n"
            "🔹 Commission ({commission_rate}%): <code>${commission_amount:.2f}</code>\n"
            "🔹 <b>Total: ${total_amount:.2f}</b>\n\n"
            "Select payment method:"
        ),
        "btn_usdt_trc20": "💰 USDT (TRC-20)",
        "btn_usdt_bep20": "💰 USDT (BEP-20)",
        "btn_bybit": "🟡 Bybit UID",
        "btn_card": "💳 Card transfer",
        "btn_lolz": "🧩 Lolz",

        # Payment details
        "payment_details": (
            "💳 <b>Order #{order_id}</b>\n\n"
            "🔹 Service: <code>{service}</code>\n"
            "🔹 Amount to pay: <b>{amount} {currency}</b>\n"
            "🔹 Payment method: <b>{method}</b>\n\n"
            "📋 <b>Payment details:</b>\n"
            "<code>{requisites}</code>\n\n"
            "After payment, click the button below:"
        ),
        "btn_paid": "✅ I paid",
        "btn_cancel_order": "❌ Cancel order",

        # Payment receipt
        "payment_receipt": (
            "✅ <b>Payment accepted!</b>\n\n"
            "🧾 <b>Order receipt #{order_id}</b>\n"
            "🔹 Amount: <code>{amount} {currency}</code>\n"
            "🔹 Payment method: <code>{method}</code>\n"
            "🔹 Date and time: <code>{datetime}</code>\n\n"
            "📝 <b>Instructions:</b>\n{instruction}\n\n"
            "⏳ Your order is being processed. Wait for admin confirmation."
        ),

        # Order management
        "order_cancelled": "❌ Order #{order_id} cancelled.",
        "active_order_exists": (
            "⚠️ You already have an active order #{order_id}.\n\n"
            "Please complete your current order before creating a new one."
        ),
        "btn_view_order": "👀 View order",
        "btn_cancel_current": "❌ Cancel order",

        # Profile
        "profile": (
            "👤 <b>My profile</b>\n\n"
            "🆔 Telegram ID: <code>{telegram_id}</code>\n"
            "🌐 Language: <code>{language}</code>\n"
            "✅ Completed orders: <code>{completed_count}</code>\n"
            "💰 Total spent: <code>${total_spent:.2f}</code>\n"
            "📅 First payment: <code>{first_payment}</code>\n"
            "📅 Last payment: <code>{last_payment}</code>"
        ),
        "btn_my_orders": "📦 My orders",
        "btn_back": "◀️ Back",

        # Orders list
        "my_orders": "📦 <b>My orders:</b>",
        "no_orders": "You don't have any orders yet.",
        "order_item": "#{id} - {service} - ${amount:.2f} - {status}",

        # Order details
        "order_details": (
            "📋 <b>Order #{id}</b>\n\n"
            "🔹 Service: <code>{service}</code>\n"
            "🔹 Base amount: <code>${base_amount:.2f}</code>\n"
            "🔹 Commission: <code>${commission:.2f}</code>\n"
            "🔹 Total: <code>${total:.2f}</code>\n"
            "🔹 Payment method: <code>{method}</code>\n"
            "🔹 Status: <code>{status}</code>\n"
            "🔹 Created: <code>{created_at}</code>"
        ),

        # Info
        "info_message": "ℹ️ <b>Information</b>\n\nSelect a section:",
        "btn_channel": "📢 Our channel",
        "btn_support": "💬 Support",
        "btn_terms": "📄 Terms of service",
        "btn_refund": "💸 Refund policy",

        # Language selection
        "select_language": "🌐 Select language / Выберите язык:",
        "language_changed": "✅ Language changed to English",

        # Status names
        "status_pending": "Pending payment",
        "status_paid_user": "Paid, awaiting verification",
        "status_completed": "Completed",
        "status_rejected": "Cancelled",

        # Payment methods
        "method_usdt_trc20": "USDT (TRC-20)",
        "method_usdt_bep20": "USDT (BEP-20)",
        "method_bybit_uid": "Bybit UID",
        "method_card": "Card transfer",
        "method_lolz": "Lolz",

        # Errors
        "user_blocked": "🚫 Your access to the bot is restricted. Contact support.",
        "error_occurred": "❌ An error occurred. Please try again later.",

        # Admin (same as Russian for now, can be translated)
        "admin_panel": "🔧 <b>Admin Panel</b>",
        "btn_stats": "📊 Statistics",
        "btn_orders": "📋 Orders",
        "btn_users": "👥 Users",
        "btn_settings": "⚙️ Settings",
        "btn_broadcast": "📢 Broadcast",

        "stats_period": "📊 Statistics for period:",
        "btn_stats_day": "Day",
        "btn_stats_week": "Week",
        "btn_stats_month": "Month",

        "stats_message": (
            "📊 <b>Statistics</b>\n\n"
            "🔹 Total orders: <code>{total_orders}</code>\n"
            "🔹 Completed: <code>{completed_orders}</code>\n"
            "🔹 Success rate: <code>{success_rate}%</code>\n"
            "🔹 Turnover (USD): <code>${total_turnover_usd:.2f}</code>\n"
            "🔹 Turnover (RUB): <code>₽{total_turnover_rub:.2f}</code>\n"
            "🔹 Commission: <code>${total_commission:.2f}</code>"
        ),

        "orders_list": "📋 <b>Orders:</b>",
        "btn_filter_all": "All",
        "btn_filter_pending": "Pending",
        "btn_filter_paid": "Paid",
        "btn_filter_completed": "Completed",

        "order_admin_details": (
            "📋 <b>Order #{id}</b>\n\n"
            "👤 User: {user_id}\n"
            "🔹 Service: {service}\n"
            "🔹 Amount: ${total:.2f}\n"
            "🔹 Method: {method}\n"
            "🔹 Status: {status}\n"
            "🔹 Created: {created_at}\n\n"
            "Change status:"
        ),

        "btn_complete": "✅ Complete",
        "btn_reject": "❌ Reject",
        "order_status_updated": "✅ Order status updated",

        # Broadcast
        "broadcast_enter_text": "📢 Enter broadcast text:",
        "broadcast_confirm": (
            "📢 <b>Broadcast</b>\n\n"
            "Text:\n{text}\n\n"
            "Send message to all users?"
        ),
        "btn_confirm": "✅ Confirm",
        "broadcast_sent": "✅ Broadcast sent to {count} users",

        # Notifications
        "new_order_notification": (
            "🔔 <b>New order #{id}</b>\n\n"
            "👤 User: {user_id}\n"
            "🔹 Service: {service}\n"
            "🔹 Amount: ${amount:.2f}\n"
            "🔹 Method: {method}"
        ),

        "payment_notification": (
            "💰 <b>Payment for order #{id}</b>\n\n"
            "👤 User: {user_id}\n"
            "🔹 Amount: {amount} {currency}\n"
            "🔹 Method: {method}\n"
            "🔹 Time: {datetime}\n\n"
            "⚠️ Requires verification!"
        ),
    }
}


def get_text(language: str, key: str, **kwargs) -> str:
    """Get text by language and key with optional formatting."""
    text = TEXTS.get(language, TEXTS["ru"]).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text
