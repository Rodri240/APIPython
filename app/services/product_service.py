from app.domain.models import Product
from app.repositories.interfaces import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self._product_repository = product_repository

    def list_products(self) -> list[Product]:
        return self._product_repository.list_all()
