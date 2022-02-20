from model import Product
from service.product_dao import ProductDao


class MaxProductDao(ProductDao):

    def get_min_valuation_item_amount(self, product: Product, price: float) -> float:
        raise NotImplementedError('get_min_valuation_item_amount')


def get_impl_clazz() -> MaxProductDao:
    return MaxProductDao
