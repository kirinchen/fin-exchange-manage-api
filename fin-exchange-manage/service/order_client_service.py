import abc
from abc import ABC
from typing import List

from sqlalchemy.orm import Session

import exchange
from dto.order_dto import OrderDto
from service.base_exchange_abc import BaseExchangeAbc
from service.product_dao import ProductDao
from utils import order_utils
from utils.order_utils import OrderFilter, OrdersInfo


class OrderClientService(BaseExchangeAbc, ABC):

    def __init__(self, exchange_name: str, session: Session = None):
        super(OrderClientService, self).__init__(exchange_name, session)
        self.productDao: ProductDao = None

    def after_init(self):
        self.productDao: ProductDao = exchange.gen_impl_obj(self.exchange_name, ProductDao, self.session)

    def get_abc_clazz(self) -> object:
        return OrderClientService

    def query_order(self, filter_obj: OrderFilter) -> OrdersInfo:
        orders = self.list_all_order(symbol=filter_obj.symbol, limit=filter_obj.limit,
                                     startTime=filter_obj.updateStartTime, endTime=filter_obj.updateEndTime)
        return order_utils.filter_order(oods=orders, ft=filter_obj)

    def clean_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        try:
            if currentOds is None:
                return list()
            if len(currentOds) <= 0:
                return list()
            self.cancel_list_orders(symbol=symbol,
                                    clientOrderIdList=[od.clientOrderId for od in currentOds])
            return currentOds
        except Exception as e:  # work on python 3.x
            print('Failed to upload to ftp: ' + str(e))

    @abc.abstractmethod
    def cancel_list_orders(self, symbol: str, clientOrderIdList: List[str]):
        raise NotImplementedError('cancel_list_orders')

    @abc.abstractmethod
    def list_all_order(self, symbol: str, orderId: int = None, startTime: int = None,
                       endTime: int = None, limit: int = None) -> List[OrderDto]:
        raise NotImplementedError('not impl')

    @abc.abstractmethod
    def post_limit(self, prd_name: str, price: float, quantity: float, positionSide: str, tags: List[str]) -> OrderDto:
        raise NotImplementedError('post_limit')

    @abc.abstractmethod
    def post_stop_market(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        raise NotImplementedError('post_stop_market')

    @abc.abstractmethod
    def post_take_profit(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        raise NotImplementedError('post_take_profit')
