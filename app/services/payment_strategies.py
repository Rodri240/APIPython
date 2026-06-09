from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class PaymentResult:
    confirmed: bool
    message: str


class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, amount: float, details: dict) -> PaymentResult:
        raise NotImplementedError


class CardPaymentStrategy(PaymentStrategy):
    def process(self, amount: float, details: dict) -> PaymentResult:
        card_token = str(details.get("card_token", "")).strip()
        if not card_token:
            return PaymentResult(confirmed=False, message="Missing card token")
        if card_token.startswith("fail"):
            return PaymentResult(confirmed=False, message="Card transaction rejected")
        return PaymentResult(confirmed=True, message=f"Card payment confirmed for {amount:.2f}")


class CashPaymentStrategy(PaymentStrategy):
    def process(self, amount: float, details: dict) -> PaymentResult:
        return PaymentResult(confirmed=True, message=f"Cash payment confirmed for {amount:.2f}")
