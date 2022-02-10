from datetime import datetime

import dateutil.parser

import exchange
from infra import database
from infra.enums import CandlestickInterval
from rest.proxy_controller import PayloadReqKey
from service.market_client_sevice import MarketClientService
from utils import comm_utils


class ParmsDto:

    def __init__(self, prd_name: str, interval: CandlestickInterval, startTime: str = None,
                 endTime: str = None, limit: int = None, **kwargs):
        self.prd_name = prd_name
        self.interval = interval
        self.startTime: datetime = dateutil.parser.parse(startTime) if startTime else None
        self.endTime: datetime = dateutil.parser.parse(endTime) if endTime else None
        self.limit = limit


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        parms_dto = ParmsDto(**payload)
        marketClient: MarketClientService = exchange.gen_impl_obj(
            exchange_name=PayloadReqKey.exchange.get_val(payload),
            clazz=MarketClientService, session=session,**payload)
        result = marketClient.get_candlestick_data(**parms_dto.__dict__)
        return comm_utils.to_dict(result)
