from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class OrderPaidEvent:
    order_id: str
    customer_id: str
    total: float


class OrderPaidObserver(Protocol):
    def notify_order_paid(self, event: OrderPaidEvent) -> None:
        ...


class EventDispatcher:
    def __init__(self) -> None:
        self._order_paid_observers: list[OrderPaidObserver] = []

    def subscribe_order_paid(self, observer: OrderPaidObserver) -> None:
        self._order_paid_observers.append(observer)

    def dispatch_order_paid(self, event: OrderPaidEvent) -> None:
        for observer in self._order_paid_observers:
            observer.notify_order_paid(event)
