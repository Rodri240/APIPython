from app.domain.exceptions import ValidationError
from app.services.payment_strategies import CardPaymentStrategy, CashPaymentStrategy, PaymentStrategy


class PaymentStrategyFactory:
    def create(self, method: str) -> PaymentStrategy:
        normalized = method.strip().lower()
        if normalized == "card":
            return CardPaymentStrategy()
        if normalized == "cash":
            return CashPaymentStrategy()
        raise ValidationError(f"Unsupported payment method: {method}. Supported methods: card, cash")
