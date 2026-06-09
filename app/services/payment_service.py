from uuid import uuid4

from app.domain.events import EventDispatcher, OrderPaidEvent
from app.domain.models import OrderStatus, Payment, PaymentStatus
from app.repositories.interfaces import OrderRepository, PaymentRepository
from app.services.payment_factory import PaymentStrategyFactory


class PaymentService:
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_repository: PaymentRepository,
        payment_factory: PaymentStrategyFactory,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self._order_repository = order_repository
        self._payment_repository = payment_repository
        self._payment_factory = payment_factory
        self._event_dispatcher = event_dispatcher

    def process_payment(self, order_id: str, method: str, details: dict) -> tuple[Payment, str]:
        order = self._order_repository.get_by_id(order_id)
        if order is None:
            raise ValueError("Order not found")
        if order.status == OrderStatus.PAID:
            raise ValueError("Order already paid")

        strategy = self._payment_factory.create(method)
        result = strategy.process(order.total, details)
        payment = Payment(
            id=str(uuid4()),
            order_id=order_id,
            method=method,
            amount=order.total,
            status=PaymentStatus.CONFIRMED if result.confirmed else PaymentStatus.REJECTED,
        )
        self._payment_repository.save(payment)

        if result.confirmed:
            order.mark_paid()
            self._order_repository.save(order)
            self._event_dispatcher.dispatch_order_paid(
                OrderPaidEvent(order_id=order.id, customer_id=order.customer_id, total=order.total)
            )

        return payment, result.message
