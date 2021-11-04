from enum import Enum


class OrderStrategy(Enum):
    TAKE_PROFIT = 'TAKE_PROFIT'
    LIMIT = 'LIMIT'
    STOP_MARKET = 'STOP_MARKET'


class PositionSide:
    BOTH = "BOTH"
    LONG = "LONG"
    SHORT = "SHORT"
    INVALID = None


class OrderSide:
    BUY = "BUY"
    SELL = "SELL"
    INVALID = None
