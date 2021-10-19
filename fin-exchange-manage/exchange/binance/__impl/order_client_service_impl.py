from typing import List

from binance_f import RequestClient
from binance_f.model import Order
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client, binance_utils
from service.order_client_service import OrderClientService


class BinanceOrderClientService(OrderClientService):

    def __init__(self, exchange: str):
        super(BinanceOrderClientService, self).__init__(exchange)
        self.client: RequestClient = gen_request_client()

    def list_all_order(self, symbol: str, orderId: int = None, startTime: int = None, endTime: int = None,
                       limit: int = None) -> List[OrderDto]:
        oods: List[Order] = self.client.get_all_orders(symbol=binance_utils.fix_usdt_symbol(symbol), limit=limit,
                                                       startTime=startTime, endTime=endTime, orderId=orderId)
        return [binance_utils.convert_order_dto(o) for o in oods]


def get_impl_clazz() -> BinanceOrderClientService:
    return BinanceOrderClientService