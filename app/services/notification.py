from app.domain.events import OrderPaidEvent, OrderPaidObserver


class CustomerNotificationService(OrderPaidObserver):
    def __init__(self) -> None:
        self.notifications: list[str] = []

    def notify_order_paid(self, event: OrderPaidEvent) -> None:
        message = f"Notification sent to customer {event.customer_id}: order {event.order_id} paid ({event.total:.2f})."
        self.notifications.append(message)
