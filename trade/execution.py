import time

import functions.dict_processing as dp
import functions.order_processing as op
import functions.signal_processing as sp
import functions.trade_processing as tp
import functions.op_management as opm
import functions.record_management as rm

from cryptofeed import FeedHandler
from cryptofeed.defines import L2_BOOK
from cryptofeed.exchanges import BinanceFutures, FTX, OKEx, HuobiSwap, Bybit, Bitmex, Bitflyer, AscendEX, Phemex, Bitfinex
from cryptofeed.exchanges.dydx import dYdX

symbols = ["BTCUSDPERP", "ETHUSDPERP", "SOLUSDPERP"]
exchanges = ["BINANCE_FUTURES", "OKEX", "BYBIT", "BITFINEX", "DYDX", "FTX", "BITMEX"]

book_trade = {symbol: {} for symbol in symbols}

async def trade(trade, receipt_timestamp):

    if "-USDT-PERP" in trade.symbol:

        symbol_id = trade.symbol.replace("-USDT-PERP", "USDPERP")

    elif "-USD-PERP" in trade.symbol:

        symbol_id = trade.symbol.replace("-USD-PERP", "USDPERP")

    book_trade[symbol_id][trade.exchange] = {

        "receipt_timestamp": receipt_timestamp,
        "exchange": trade.exchange,
        "symbol": trade.symbol,
        "side": trade.side,
        "price": float(trade.price),
        "amount": float(trade.amount)

    }

    if trade.side == "sell":

        

    if opm.order_database.hexists(symbol_id, trade.exchange):

        order = opm.order_database.hmget(symbol_id, trade.exchange)

        maker_exchange = max(open_p, key = lambda x: open_p[x]["maker"]["price"])
        taker_exchange = min(order[symbol_id][trade.exchange], key = lambda x: order[symbol_id][trade.exchange][x]["maker"]["price"])

