import time

def taker_respons(symbol_id, order, exchange):

    trade_d = {}

    trade_d[symbol_id] = {

        "order_time": order["order_time"],
        "receipt_time": order["receipt_time"],
        "trade_time": time.time(),
        "symbol": symbol_id,
        "exchange": exchange,
        "type": order["type"],
        "side": order["side"],
        "order_price": order["price"],
        "order_amount": order["amount"],
        "total_order_value": order["price"] * order["amount"],
        "trade_price": order["price"],
        "trade_amount": order["amount"],
        "total_trade_value": order["price"] * order["amount"],
        "strategy": order["strategy"]

    }

    return trade_d

def maker_respons(symbol_id, order, trade, exchange):

    trade_d = {}

    trade = trade[symbol_id][exchange]

    trade_d[symbol_id] = {

        "order_time": order["order_time"],
        "receipt_time": order["receipt_time"],
        "trade_time": time.time(),
        "symbol": symbol_id,
        "exchange": exchange,
        "type": order["type"],
        "side": order["side"],
        "order_price": order["price"],
        "order_amount": order["amount"],
        "total_order_value": order["price"] * order["amount"],
        "trade_price": trade["price"],
        "trade_amount": trade["amount"],
        "total_trade_value": trade["price"] * trade["amount"],
        "strategy": order["strategy"]

    }

    return trade_d

def maker_taker_respons(symbol_id, taker_order, maker_trade, taker_exchange):

    trade_d = {}

    taker_order = taker_order
    maker_trade = maker_trade[symbol_id]

    trade_d[symbol_id] = {

        "order_time": taker_order["order_time"],
        "receipt_time": taker_order["receipt_time"],
        "trade_time": time.time(),
        "symbol": symbol_id,
        "exchange": taker_exchange,
        "type": taker_order["type"],
        "side": taker_order["side"],
        "order_price": taker_order["price"],
        "order_amount": taker_order["amount"],
        "total_order_value": taker_order["price"] * taker_order["price"],
        "trade_price": taker_order["price"],
        "trade_amount": maker_trade["trade_amount"],
        "total_trade_value": taker_order["price"] * maker_trade["trade_amount"],
        "strategy": taker_order["strategy"]

    }

    return trade_d