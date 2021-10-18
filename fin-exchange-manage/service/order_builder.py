from abc import ABCMeta, ABC
from typing import TypeVar, Generic

from dto.post_order_dto import BasePostOrderDto
from service.base_exchange_abc import BaseExchangeAbc

T = TypeVar('T', bound=BasePostOrderDto)


class BaseOrderBuilder(Generic[T], BaseExchangeAbc, ABC):

    def __init__(self,  dto: T):
        self.dto: T = dto

    def get_current_position(self) -> Position:
        result: List[Position] = self.client.get_position()
        pf = PositionFilter(symbol=self.dto.symbol, positionSide=self.dto.positionSide)
        result = position_utils.filter_position(result, pf)
        return result[0]

    def post(self) -> List[Order]:
        ans: List[Order] = list()
        for pq in self.gen_price_qty_list():
            ans.append(self.post_one(pq))
        return ans

    @abc.abstractmethod
    def load_data(self) -> LoadDataCheck:
        return NotImplemented

    @abc.abstractmethod
    def get_order_side(self) -> str:
        return NotImplemented

    @abc.abstractmethod
    def gen_price_qty_list(self) -> List[PriceQty]:
        return NotImplemented

    @abc.abstractmethod
    def post_one(self, pq: PriceQty) -> Order:
        return NotImplemented
