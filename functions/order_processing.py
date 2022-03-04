import time
'''

function:

mt_order, tm_order, tt_order

return:

order[symbol_id]:{

    "buy_order": {
    
        "bid_exchange": bid_exchange,
        "ask_exchange": ask_exchange,
        "receipt_time": book[symbol_id][bid_exchange]["receipt_timestamp"],
        "order_time": time.time(),
        "symbol": symbol_id,
        "type": "limit",
        "side": "buy",
        "amount": min(book[symbol_id][bid_exchange]["bid_size"],
                      book[symbol_id][ask_exchange]["bid_size"]),
        "price": book[symbol_id][bid_exchange]["bid"],
        "strategy": "NBBOMT"
    
    },
    
    "sell_order": {

        "bid_exchange": bid_exchange,
        "ask_exchange": ask_exchange,
        "receipt_time": book[symbol_id][ask_exchange]["receipt_timestamp"],
        "order_time": time.time(),
        "symbol": symbol_id,
        "type": "limit",
        "side": "sell",
        "amount": min(book[symbol_id][bid_exchange]["bid_size"],
                    book[symbol_id][ask_exchange]["bid_size"]),
        "price": book[symbol_id][ask_exchange]["bid"],
        "strategy": "NBBOMT"

    },

}

function:

all_order(mt_order, tm_order, tt_order)

return:

order[symbol_id] = {

    "NBBOMT": {

        "buy_order": {

            nbbo[symbol_id]["NBBOMT"]["bid_exchange"]: {

                "bid_exchange": mt_bid_exchange,
                "ask_exchange": mt_ask_exchange,
                "receipt_time": book[symbol_id][mt_bid_exchange]["receipt_timestamp"],
                "order_time": time.time(),
                "symbol": symbol_id,
                "type": "limit",
                "side": "buy",
                "amount": min(book[symbol_id][mt_bid_exchange]["ask_size"],
                            book[symbol_id][mt_ask_exchange]["bid_size"]),
                "price": book[symbol_id][mt_bid_exchange]["ask"],
                "strategy": "NBBOTT"

            }

        },

        "sell_order": {

            "bid_exchange": mt_bid_exchange,
            "ask_exchange": mt_ask_exchange,
            "receipt_time": book[symbol_id][mt_ask_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "sell",
            "amount": min(book[symbol_id][mt_bid_exchange]["bid_size"],
                        book[symbol_id][mt_ask_exchange]["bid_size"]),
            "price": book[symbol_id][mt_ask_exchange]["bid"],
            "strategy": "NBBOMT"

        }

    },

    "NBBOTM": {

        "buy_order": {

            "bid_exchange": tm_bid_exchange,
            "ask_exchange": tm_ask_exchange,
            "receipt_time": book[symbol_id][tm_bid_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "buy",
            "amount": min(book[symbol_id][tm_bid_exchange]["ask_size"],
                        book[symbol_id][tm_ask_exchange]["ask_size"]),
            "price": book[symbol_id][tm_bid_exchange]["ask"],
            "strategy": "NBBOTM"

        },

        "sell_order": {

            "bid_exchange": tm_bid_exchange,
            "ask_exchange": tm_ask_exchange,
            "receipt_time": book[symbol_id][tm_ask_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "sell",
            "amount": min(book[symbol_id][tm_bid_exchange]["ask_size"],
                        book[symbol_id][tm_ask_exchange]["ask_size"]),
            "price": book[symbol_id][tm_ask_exchange]["ask"],
            "strategy": "NBBOTM"

        }

    },

    "NBBOTT": {

        "buy_order": {

            "buy_order": tt_bid_exchange,
            "sell_order": tt_ask_exchange,
            "receipt_time": book[symbol_id][tt_bid_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "buy",
            "amount": min(book[symbol_id][tt_bid_exchange]["ask_size"],
                        book[symbol_id][tt_ask_exchange]["bid_size"]),
            "price": book[symbol_id][tt_bid_exchange]["ask"],
            "strategy": "NBBOTT"

        },

        "sell_order": {

            "buy_order": tt_bid_exchange,
            "sell_order": tt_ask_exchange,
            "receipt_time": book[symbol_id][tt_ask_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "sell",
            "amount": min(book[symbol_id][tt_bid_exchange]["ask_size"],
                        book[symbol_id][tt_ask_exchange]["bid_size"]),
            "price": book[symbol_id][tt_ask_exchange]["bid"],
            "strategy": "NBBOTT"

        }

    }

}

'''
def mt_order(symbol_id, book, nbbo):

    order = {}

    maker_exchange = nbbo[symbol_id]["NBBOMT"]["bid_exchange"]
    taker_exchange = nbbo[symbol_id]["NBBOMT"]["ask_exchange"]

    order[symbol_id] = {

        "buy_order": {

            "maker_exchange": maker_exchange,
            "taker_exchange": taker_exchange,
            "receipt_time": book[symbol_id][maker_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "buy",
            "amount": min(book[symbol_id][maker_exchange]["bid_size"],
                          book[symbol_id][taker_exchange]["bid_size"]),
            "price": book[symbol_id][maker_exchange]["bid"],
            "strategy": "NBBOMT"

        },

        "sell_order": {

            "maker_exchange": maker_exchange,
            "taker_exchange": taker_exchange,
            "receipt_time": book[symbol_id][taker_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "sell",
            "amount": min(book[symbol_id][maker_exchange]["bid_size"],
                        book[symbol_id][taker_exchange]["bid_size"]),
            "price": book[symbol_id][taker_exchange]["bid"],
            "strategy": "NBBOMT"

        },

    }

    return order, maker_exchange, taker_exchange

def tm_order(symbol_id, book, nbbo):
    order = {}

    taker_exchange = nbbo[symbol_id]["NBBOTM"]["bid_exchange"]
    maker_exchange = nbbo[symbol_id]["NBBOTM"]["ask_exchange"]

    order[symbol_id] = {

        "buy_order": {

            "taker_exchange": taker_exchange,
            "maker_exchange": maker_exchange,
            "receipt_time": book[symbol_id][taker_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "buy",
            "amount": min(book[symbol_id][taker_exchange]["ask_size"],
                          book[symbol_id][maker_exchange]["ask_size"]),
            "price": book[symbol_id][taker_exchange]["ask"],
            "strategy": "NBBOTM"

        },

        "sell_order": {

            "taker_exchange": taker_exchange,
            "maker_exchange": maker_exchange,
            "receipt_time": book[symbol_id][maker_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "sell",
            "amount": min(book[symbol_id][taker_exchange]["ask_size"],
                          book[symbol_id][maker_exchange]["ask_size"]),
            "price": book[symbol_id][maker_exchange]["ask"],
            "strategy": "NBBOTM"

        }

    }

    return order, maker_exchange, taker_exchange

def tt_order(symbol_id, book, nbbo):

    order = {}

    maker_exchange = nbbo[symbol_id]["NBBOTT"]["bid_exchange"]
    taker_exchange = nbbo[symbol_id]["NBBOTT"]["ask_exchange"]

    order[symbol_id] = {

        "buy_order": {

            "maker_exchange": maker_exchange,
            "taker_exchange": taker_exchange,
            "receipt_time": book[symbol_id][maker_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "buy",
            "amount": min(book[symbol_id][maker_exchange]["ask_size"],
                        book[symbol_id][taker_exchange]["bid_size"]),
            "price": book[symbol_id][maker_exchange]["ask"],
            "strategy": "NBBOTT"

        },

        "sell_order": {

            "maker_exchange": maker_exchange,
            "taker_exchange": taker_exchange,
            "receipt_time": book[symbol_id][taker_exchange]["receipt_timestamp"],
            "order_time": time.time(),
            "symbol": symbol_id,
            "type": "limit",
            "side": "sell",
            "amount": min(book[symbol_id][maker_exchange]["ask_size"],
                          book[symbol_id][taker_exchange]["bid_size"]),
            "price": book[symbol_id][taker_exchange]["bid"],
            "strategy": "NBBOTT"

        },

    }

    return order, maker_exchange, taker_exchange

def all_order(symbol_id, book, nbbo):

    order = {}

    mt_bid_exchange = nbbo[symbol_id]["NBBOMT"]["bid_exchange"]
    mt_ask_exchange = nbbo[symbol_id]["NBBOMT"]["ask_exchange"]
    tm_bid_exchange = nbbo[symbol_id]["NBBOTM"]["bid_exchange"]
    tm_ask_exchange = nbbo[symbol_id]["NBBOTM"]["ask_exchange"]
    tt_bid_exchange = nbbo[symbol_id]["NBBOTT"]["bid_exchange"]
    tt_ask_exchange = nbbo[symbol_id]["NBBOTT"]["ask_exchange"]

    order[symbol_id] = {

        "NBBOMT": {

            "buy_order": {

                nbbo[symbol_id]["NBBOMT"]["bid_exchange"]: {

                    "bid_exchange": mt_bid_exchange,
                    "ask_exchange": mt_ask_exchange,
                    "receipt_time": book[symbol_id][mt_bid_exchange]["receipt_timestamp"],
                    "order_time": time.time(),
                    "symbol": symbol_id,
                    "type": "limit",
                    "side": "buy",
                    "amount": min(book[symbol_id][mt_bid_exchange]["ask_size"],
                                book[symbol_id][mt_ask_exchange]["bid_size"]),
                    "price": book[symbol_id][mt_bid_exchange]["ask"],
                    "strategy": "NBBOTT"

                }

            },

            "sell_order": {

                "bid_exchange": mt_bid_exchange,
                "ask_exchange": mt_ask_exchange,
                "receipt_time": book[symbol_id][mt_ask_exchange]["receipt_timestamp"],
                "order_time": time.time(),
                "symbol": symbol_id,
                "type": "limit",
                "side": "sell",
                "amount": min(book[symbol_id][mt_bid_exchange]["bid_size"],
                            book[symbol_id][mt_ask_exchange]["bid_size"]),
                "price": book[symbol_id][mt_ask_exchange]["bid"],
                "strategy": "NBBOMT"

            }

        },

        "NBBOTM": {

            "buy_order": {

                "bid_exchange": tm_bid_exchange,
                "ask_exchange": tm_ask_exchange,
                "receipt_time": book[symbol_id][tm_bid_exchange]["receipt_timestamp"],
                "order_time": time.time(),
                "symbol": symbol_id,
                "type": "limit",
                "side": "buy",
                "amount": min(book[symbol_id][tm_bid_exchange]["ask_size"],
                            book[symbol_id][tm_ask_exchange]["ask_size"]),
                "price": book[symbol_id][tm_bid_exchange]["ask"],
                "strategy": "NBBOTM"

            },

            "sell_order": {

                "bid_exchange": tm_bid_exchange,
                "ask_exchange": tm_ask_exchange,
                "receipt_time": book[symbol_id][tm_ask_exchange]["receipt_timestamp"],
                "order_time": time.time(),
                "symbol": symbol_id,
                "type": "limit",
                "side": "sell",
                "amount": min(book[symbol_id][tm_bid_exchange]["ask_size"],
                            book[symbol_id][tm_ask_exchange]["ask_size"]),
                "price": book[symbol_id][tm_ask_exchange]["ask"],
                "strategy": "NBBOTM"

            }

        },

        "NBBOTT": {

            "buy_order": {

                "buy_order": tt_bid_exchange,
                "sell_order": tt_ask_exchange,
                "receipt_time": book[symbol_id][tt_bid_exchange]["receipt_timestamp"],
                "order_time": time.time(),
                "symbol": symbol_id,
                "type": "limit",
                "side": "buy",
                "amount": min(book[symbol_id][tt_bid_exchange]["ask_size"],
                            book[symbol_id][tt_ask_exchange]["bid_size"]),
                "price": book[symbol_id][tt_bid_exchange]["ask"],
                "strategy": "NBBOTT"

            },

            "sell_order": {

                "buy_order": tt_bid_exchange,
                "sell_order": tt_ask_exchange,
                "receipt_time": book[symbol_id][tt_ask_exchange]["receipt_timestamp"],
                "order_time": time.time(),
                "symbol": symbol_id,
                "type": "limit",
                "side": "sell",
                "amount": min(book[symbol_id][tt_bid_exchange]["ask_size"],
                            book[symbol_id][tt_ask_exchange]["bid_size"]),
                "price": book[symbol_id][tt_ask_exchange]["bid"],
                "strategy": "NBBOTT"

            }

        }

    }

    return order
