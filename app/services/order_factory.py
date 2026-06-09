from app.domain.models import Order, OrderItem, Product
from app.domain.exceptions import NotFoundError, ValidationError


class OrderFactory:
    def create(self, order_id: str, customer_id: str, requested_items: list[dict], products: dict[str, Product]) -> Order:
        if not requested_items:
            raise ValidationError("Order must contain at least one item")

        items: list[OrderItem] = []
        for item in requested_items:
            product_id = item["product_id"]
            quantity = item["quantity"]

            if quantity <= 0:
                raise ValidationError(f"Quantity must be positive for product {product_id}, got {quantity}")

            product = products.get(product_id)
            if product is None:
                raise NotFoundError(f"Product not found: {product_id}")

            items.append(OrderItem(product_id=product.id, quantity=quantity, unit_price=product.price))

        order = Order(id=order_id, customer_id=customer_id, items=items)
        order.recalculate_total()
        return order
