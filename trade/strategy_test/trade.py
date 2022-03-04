import time
import ast
from tkinter.tix import Tree

import redis

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

        order = opm.mt_orders.hmget(symbol_id, trade.exchange)
        max_pair = max(order, key = lambda x: order[x]["maker"]["price"])
        trade_order = ast.literal_eval(order[0].decode("utf-8"))

        maker_order, taker_order = trade_order[max_pair]["maker"], trade_order[max_pair]["taker"]
        maker_exchange, taker_exchange = maker_order["maker_exchange"], taker_order["taker_exchange"]

        if trade.price < maker_order["price"]:

            maker_respons = tp.maker_respons(symbol_id, maker_order, book_trade, maker_exchange)
            taker_respons = tp.maker_respons(symbol_id, taker_exchange, book_trade, maker_exchange)

            opm.open_positions(symbol_id, maker_respons, maker_exchange)
            opm.open_positions(symbol_id, taker_respons, taker_exchange)
            opm.open_spositions(symbol_id, maker_respons, taker_respons, maker_exchange, taker_exchange)

            rm.q_new_trade(symbol_id, maker_respons, "new")
            rm.q_new_trade(symbol_id, taker_respons, "new")

            '''
            if opm.position_database.hexists(symbol_id, maker_exchange) == True and opm.position_database.hexists(symbol_id, taker_exchange) == True:

                opm.open_positions(symbol_id, maker_respons, maker_exchange)
                opm.open_positions(symbol_id, taker_respons, taker_exchange)

                opm.mtorder_update(symbol_id, max_pair, maker_exchange)

            elif opm.position_database.hexists(symbol_id, maker_exchange) == True and opm.position_database.hexists(symbol_id, taker_exchange) == False:

                opm.open_positions(symbol_id, maker_respons, maker_exchange)
                opm.open_positions(symbol_id, taker_respons, taker_exchange)

                opm.mtorder_update(symbol_id, max_pair, maker_exchange)        

            elif opm.position_database.hexists(symbol_id, maker_exchange) == False and opm.position_database.hexists(symbol_id, taker_exchange) == True:

                opm.open_positions(symbol_id, maker_respons, maker_exchange)
                opm.open_positions(symbol_id, taker_respons, taker_exchange)

                opm.mtorder_update(symbol_id, max_pair, maker_exchange)

            else:

                opm.open_positions(symbol_id, maker_respons, maker_exchange)
                opm.open_positions(symbol_id, taker_respons, taker_exchange)

                opm.mtorder_update(symbol_id, max_pair, maker_exchange)           
        '''     
    elif trade.side == "buy":

         order = opm.tm_orders.hmget(symbol_id, trade.exchange)
