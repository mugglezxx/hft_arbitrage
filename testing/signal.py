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
open_order = orders = {symbol: {exchange: {}for exchange in exchanges} for symbol in symbols}

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

    nbbo_book = sp.mkt_nbbo(book_price, symbol_id)

    start = time.time()

    if nbbo_book[symbol_id]["NBBOTT"]["spread"] > nbbo_book[symbol_id]["NBBOTT"]["signal"]:

        order, maker_exchange, taker_exchange = op.tt_order(symbol_id, book_price, nbbo_book)
        
        buy_order = order[symbol_id]["buy_order"]
        sell_order = order[symbol_id]["sell_order"]

        buy_respons = tp.taker_respons(symbol_id, buy_order, maker_exchange)
        sell_respons = tp.taker_respons(symbol_id, sell_order, taker_exchange)

        opm.open_positions(symbol_id, buy_respons, maker_exchange)
        opm.open_positions(symbol_id, sell_respons, taker_exchange)
        opm.strat_positions(symbol_id, buy_respons, sell_respons, maker_exchange, taker_exchange)

        rm.q_new_order(symbol_id, buy_order, maker_exchange, "new")
        rm.q_new_order(symbol_id, sell_order, taker_exchange, "new")

        rm.q_new_trade(symbol_id, buy_respons, "open")
        rm.q_new_trade(symbol_id, sell_respons, "open")

    if nbbo_book[symbol_id]["NBBOMT"]["spread"] > nbbo_book[symbol_id]["NBBOMT"]["signal"]:

        order, maker_exchange, taker_exchange = op.mt_order(symbol_id, book_price, nbbo_book)
        
        buy_order = order[symbol_id]["buy_order"]
        sell_order = order[symbol_id]["sell_order"]
        
        dp.update_dict(symbol_id, open_order, buy_order, sell_order, maker_exchange, taker_exchange)

        opm.open_orders(symbol_id, open_order[symbol_id])

        #rm.q_new_order(symbol_id, buy_order, maker_exchange, "new")
        #rm.q_new_order(symbol_id, sell_order, taker_exchange, "new")

    if nbbo_book[symbol_id]["NBBOTM"]["spread"] > nbbo_book[symbol_id]["NBBOTM"]["signal"]:

        order, maker_exchange, taker_exchange = op.tm_order(symbol_id, book_price, nbbo_book)

        buy_order = order[symbol_id]["buy_order"]
        sell_order = order[symbol_id]["sell_order"]

        dp.update_dict(symbol_id, open_order, sell_order, buy_order, maker_exchange, taker_exchange)

        opm.open_orders(symbol_id, open_order[symbol_id])

        #rm.q_new_order(symbol_id, buy_order, maker_exchange, "new")
        #rm.q_new_order(symbol_id, sell_order, taker_exchange, "new")
    
    print(time.time() - start)

def main():

    data_feed = FeedHandler()

    data_feed.add_feed(BinanceFutures(symbols = ["BTC-USDT-PERP", "ETH-USDT-PERP", "SOL-USDT-PERP"], channels = [L2_BOOK], callbacks = {L2_BOOK: order_book}))
    data_feed.add_feed(Bybit(symbols = ["BTC-USDT-PERP", "ETH-USDT-PERP", "SOL-USDT-PERP"], channels = [L2_BOOK], callbacks = {L2_BOOK: order_book}))
    data_feed.add_feed(OKEx(symbols = ["BTC-USDT-PERP", "ETH-USDT-PERP", "SOL-USDT-PERP"], channels = [L2_BOOK], callbacks = {L2_BOOK: order_book}))
    data_feed.add_feed(Bitmex(symbols = ["BTC-USDT-PERP", "ETH-USDT-PERP", "SOL-USDT-PERP"], channels = [L2_BOOK], callbacks = {L2_BOOK: order_book}))
    data_feed.add_feed(Bitfinex(symbols = ["BTC-USDT-PERP", "ETH-USDT-PERP", "SOL-USDT-PERP"], channels = [L2_BOOK], callbacks = {L2_BOOK: order_book}))
    data_feed.add_feed(dYdX(symbols = ["BTC-USD-PERP", "ETH-USD-PERP", "SOL-USD-PERP"], channels = [L2_BOOK], callbacks = {L2_BOOK: order_book}, cross_check = True))
    data_feed.add_feed(FTX(symbols = ["BTC-USD-PERP", "ETH-USD-PERP", "SOL-USD-PERP"], channels = [L2_BOOK], callbacks = {L2_BOOK: order_book}))

    data_feed.run()

if __name__ == '__main__':

    main()