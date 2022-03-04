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

book_price = {symbol: {} for symbol in symbols}
open_order = {symbol: {exchange: {}for exchange in exchanges} for symbol in symbols}

async def order_book(book, receipt_timestamp):

    if "-USDT-PERP" in book.symbol:

        symbol_id = book.symbol.replace("-USDT-PERP", "USDPERP")

    elif "-USD-PERP" in book.symbol:

        symbol_id = book.symbol.replace("-USD-PERP", "USDPERP")

    book_price[symbol_id][book.exchange] = {

        "receipt_timestamp": receipt_timestamp,
        "bid": float(book.book.bids.index(0)[0]),
        "ask": float(book.book.asks.index(0)[0]),
        "bid_size": float(book.book.bids.index(0)[1]),
        "ask_size": float(book.book.asks.index(0)[1])

    }

    