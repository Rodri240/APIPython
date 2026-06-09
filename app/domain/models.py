from dataclasses import dataclass
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"


class PaymentStatus(str, Enum):
    REJECTED = "rejected"
    CONFIRMED = "confirmed"


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price: float


@dataclass(frozen=True)
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return round(self.quantity * self.unit_price, 2)


@dataclass
class Order:
    id: str
    customer_id: str
    items: list[OrderItem]
    total: float = 0.0
    status: OrderStatus = OrderStatus.PENDING

    def recalculate_total(self) -> None:
        self.total = round(sum(item.subtotal for item in self.items), 2)

    def mark_paid(self) -> None:
        self.status = OrderStatus.PAID


@dataclass
class Payment:
    id: str
    order_id: str
    method: str
    amount: float
    status: PaymentStatus
