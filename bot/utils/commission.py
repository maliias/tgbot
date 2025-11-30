"""Commission calculation utilities."""
from decimal import Decimal
from typing import Tuple


def calculate_commission(base_amount: Decimal) -> Tuple[Decimal, Decimal]:
    """
    Calculate commission based on amount.

    Commission structure:
    - S ≤ $10 → 15%, but not less than $1.5
    - $10 < S ≤ $20 → 12%, but not less than $1.5
    - $20 < S ≤ $35 → 10%
    - $35 < S ≤ $50 → 8%
    - $50 < S ≤ $75 → 6%
    - $75 < S ≤ $250 → 5%
    - S > $250 → 3%

    Returns:
        Tuple[commission_rate, commission_amount]
    """
    amount = float(base_amount)

    if amount <= 10:
        rate = Decimal("15.0")
        commission = max(base_amount * rate / 100, Decimal("1.5"))
    elif amount <= 20:
        rate = Decimal("12.0")
        commission = max(base_amount * rate / 100, Decimal("1.5"))
    elif amount <= 35:
        rate = Decimal("10.0")
        commission = base_amount * rate / 100
    elif amount <= 50:
        rate = Decimal("8.0")
        commission = base_amount * rate / 100
    elif amount <= 75:
        rate = Decimal("6.0")
        commission = base_amount * rate / 100
    elif amount <= 250:
        rate = Decimal("5.0")
        commission = base_amount * rate / 100
    else:
        rate = Decimal("3.0")
        commission = base_amount * rate / 100

    return rate, commission


def calculate_payment_amount(
    total_amount: Decimal,
    payment_method: str,
    usd_to_rub_rate: float
) -> Tuple[Decimal, str]:
    """
    Calculate payment amount based on payment method.

    Args:
        total_amount: Total amount in USD
        payment_method: Payment method (USDT_TRC20, USDT_BEP20, BYBIT_UID, CARD, LOLZ)
        usd_to_rub_rate: USD to RUB exchange rate

    Returns:
        Tuple[payment_amount, currency]
    """
    if payment_method == "CARD":
        # Convert to RUB and round to whole number
        payment_amount = Decimal(str(round(float(total_amount) * usd_to_rub_rate)))
        currency = "RUB"
    elif payment_method == "LOLZ":
        # Add 4% commission for Lolz
        payment_amount = total_amount * Decimal("1.04")
        currency = "USD"
    else:  # USDT_TRC20, USDT_BEP20, BYBIT_UID
        # Keep in USD/USDT
        payment_amount = total_amount
        currency = "USDT"

    # Round to 2 decimal places
    payment_amount = payment_amount.quantize(Decimal("0.01"))

    return payment_amount, currency
