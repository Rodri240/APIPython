from fastapi import FastAPI, HTTPException

from app.domain.models import Order
from app.repositories.in_memory import InMemoryOrderRepository, InMemoryPaymentRepository, InMemoryProductRepository
from app.schemas import (
    CreateOrderRequest,
    OrderItemResponse,
    OrderResponse,
    PaymentRequest,
    PaymentResponse,
    ProductResponse,
)
from app.services.notification import CustomerNotificationService
from app.services.order_factory import OrderFactory
from app.services.order_service import OrderService
from app.services.payment_factory import PaymentStrategyFactory
from app.services.payment_service import PaymentService
from app.domain.events import EventDispatcher

app = FastAPI(title="Order Payment API", version="1.0.0")

product_repository = InMemoryProductRepository()
order_repository = InMemoryOrderRepository()
payment_repository = InMemoryPaymentRepository()
event_dispatcher = EventDispatcher()

notification_service = CustomerNotificationService()
event_dispatcher.subscribe_order_paid(notification_service)

order_service = OrderService(
    product_repository=product_repository,
    order_repository=order_repository,
    order_factory=OrderFactory(),
)
payment_service = PaymentService(
    order_repository=order_repository,
    payment_repository=payment_repository,
    payment_factory=PaymentStrategyFactory(),
    event_dispatcher=event_dispatcher,
)


def _to_order_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        status=order.status.value,
        total=order.total,
        items=[
            OrderItemResponse(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
            )
            for item in order.items
        ],
    )


@app.get("/products", response_model=list[ProductResponse])
def list_products() -> list[ProductResponse]:
    return [ProductResponse(id=p.id, name=p.name, price=p.price) for p in order_service.list_products()]


@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(payload: CreateOrderRequest) -> OrderResponse:
    try:
        order = order_service.create_order(
            customer_id=payload.customer_id,
            items=[{"product_id": i.product_id, "quantity": i.quantity} for i in payload.items],
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return _to_order_response(order)


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: str) -> OrderResponse:
    try:
        order = order_service.get_order(order_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return _to_order_response(order)


@app.post("/orders/{order_id}/payments", response_model=PaymentResponse)
def process_order_payment(order_id: str, payload: PaymentRequest) -> PaymentResponse:
    try:
        payment, message = payment_service.process_payment(order_id=order_id, method=payload.method, details=payload.details)
    except ValueError as error:
        detail = str(error)
        status_code = 404 if detail == "Order not found" else 400
        raise HTTPException(status_code=status_code, detail=detail) from error

    return PaymentResponse(
        id=payment.id,
        order_id=payment.order_id,
        amount=payment.amount,
        method=payment.method,
        status=payment.status.value,
        message=message,
    )
