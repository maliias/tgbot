"""Order model and database operations."""
from datetime import datetime
from typing import Optional, List, Tuple
from decimal import Decimal
import asyncpg


class OrderStatus:
    """Order status constants."""
    PENDING = "PENDING"              # Ожидает оплаты
    PAID_USER = "PAID_USER"          # Оплачен пользователем
    COMPLETED = "COMPLETED"          # Успешно выполнен
    REJECTED = "REJECTED"            # Отменен


class PaymentMethod:
    """Payment method constants."""
    USDT_TRC20 = "USDT_TRC20"
    USDT_BEP20 = "USDT_BEP20"
    BYBIT_UID = "BYBIT_UID"
    CARD = "CARD"
    LOLZ = "LOLZ"


class Order:
    """Order model."""

    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = None,
        service_name: str = None,
        base_amount: Decimal = None,
        commission_rate: Decimal = None,
        commission_amount: Decimal = None,
        total_amount: Decimal = None,
        payment_method: str = None,
        payment_amount: Decimal = None,
        payment_currency: str = None,
        status: str = OrderStatus.PENDING,
        created_at: Optional[datetime] = None,
        paid_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.service_name = service_name
        self.base_amount = base_amount
        self.commission_rate = commission_rate
        self.commission_amount = commission_amount
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.payment_amount = payment_amount
        self.payment_currency = payment_currency
        self.status = status
        self.created_at = created_at
        self.paid_at = paid_at
        self.completed_at = completed_at
        self.updated_at = updated_at

    @classmethod
    def from_record(cls, record: asyncpg.Record) -> "Order":
        """Create Order instance from database record."""
        return cls(
            id=record["id"],
            user_id=record["user_id"],
            service_name=record["service_name"],
            base_amount=record["base_amount"],
            commission_rate=record["commission_rate"],
            commission_amount=record["commission_amount"],
            total_amount=record["total_amount"],
            payment_method=record["payment_method"],
            payment_amount=record["payment_amount"],
            payment_currency=record["payment_currency"],
            status=record["status"],
            created_at=record["created_at"],
            paid_at=record["paid_at"],
            completed_at=record["completed_at"],
            updated_at=record["updated_at"]
        )


class OrderRepository:
    """Order database operations."""

    def __init__(self, db):
        self.db = db

    async def create(self, order: Order) -> Order:
        """Create new order."""
        query = """
            INSERT INTO orders (
                user_id, service_name, base_amount, commission_rate,
                commission_amount, total_amount, payment_method,
                payment_amount, payment_currency, status
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING *
        """
        record = await self.db.fetchrow(
            query,
            order.user_id,
            order.service_name,
            order.base_amount,
            order.commission_rate,
            order.commission_amount,
            order.total_amount,
            order.payment_method,
            order.payment_amount,
            order.payment_currency,
            order.status
        )
        return Order.from_record(record)

    async def get(self, order_id: int) -> Optional[Order]:
        """Get order by ID."""
        query = "SELECT * FROM orders WHERE id = $1"
        record = await self.db.fetchrow(query, order_id)
        return Order.from_record(record) if record else None

    async def get_user_orders(
        self,
        user_id: int,
        limit: int = 10,
        offset: int = 0
    ) -> List[Order]:
        """Get user orders."""
        query = """
            SELECT * FROM orders
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2 OFFSET $3
        """
        records = await self.db.fetch(query, user_id, limit, offset)
        return [Order.from_record(record) for record in records]

    async def get_active_order(self, user_id: int) -> Optional[Order]:
        """Get user's active order (PENDING or PAID_USER status)."""
        query = """
            SELECT * FROM orders
            WHERE user_id = $1 AND status IN ('PENDING', 'PAID_USER')
            ORDER BY created_at DESC
            LIMIT 1
        """
        record = await self.db.fetchrow(query, user_id)
        return Order.from_record(record) if record else None

    async def update_status(
        self,
        order_id: int,
        status: str,
        paid_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None
    ):
        """Update order status."""
        query = """
            UPDATE orders
            SET status = $1, paid_at = COALESCE($2, paid_at),
                completed_at = COALESCE($3, completed_at)
            WHERE id = $4
        """
        await self.db.execute(query, status, paid_at, completed_at, order_id)

    async def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics."""
        query = """
            SELECT
                COUNT(*) FILTER (WHERE status = 'COMPLETED') as completed_count,
                COALESCE(SUM(total_amount) FILTER (WHERE status = 'COMPLETED'), 0) as total_spent,
                MIN(created_at) FILTER (WHERE status = 'COMPLETED') as first_payment,
                MAX(created_at) FILTER (WHERE status = 'COMPLETED') as last_payment
            FROM orders
            WHERE user_id = $1
        """
        record = await self.db.fetchrow(query, user_id)
        return {
            "completed_count": record["completed_count"] or 0,
            "total_spent": float(record["total_spent"]) or 0.0,
            "first_payment": record["first_payment"],
            "last_payment": record["last_payment"]
        }

    async def get_all_orders(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Order]:
        """Get all orders with optional status filter."""
        if status:
            query = """
                SELECT * FROM orders
                WHERE status = $1
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3
            """
            records = await self.db.fetch(query, status, limit, offset)
        else:
            query = """
                SELECT * FROM orders
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
            """
            records = await self.db.fetch(query, limit, offset)

        return [Order.from_record(record) for record in records]

    async def get_stats(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Get statistics for period."""
        query = """
            SELECT
                COUNT(*) as total_orders,
                COUNT(*) FILTER (WHERE status = 'COMPLETED') as completed_orders,
                COALESCE(SUM(total_amount), 0) as total_turnover_usd,
                COALESCE(SUM(commission_amount), 0) as total_commission_usd,
                COALESCE(SUM(payment_amount) FILTER (WHERE payment_currency = 'RUB'), 0) as total_turnover_rub
            FROM orders
            WHERE created_at >= $1 AND created_at <= $2
        """
        record = await self.db.fetchrow(query, start_date, end_date)
        total = record["total_orders"] or 0
        completed = record["completed_orders"] or 0

        return {
            "total_orders": total,
            "completed_orders": completed,
            "success_rate": round((completed / total * 100) if total > 0 else 0, 2),
            "total_turnover_usd": float(record["total_turnover_usd"]) or 0.0,
            "total_turnover_rub": float(record["total_turnover_rub"]) or 0.0,
            "total_commission": float(record["total_commission_usd"]) or 0.0
        }

    async def get_paid_user_orders(self) -> List[Order]:
        """Get orders with PAID_USER status for admin review."""
        query = """
            SELECT * FROM orders
            WHERE status = 'PAID_USER'
            ORDER BY paid_at DESC
        """
        records = await self.db.fetch(query)
        return [Order.from_record(record) for record in records]
