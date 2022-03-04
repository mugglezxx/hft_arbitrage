def update_dict(symbol_id, open_order, maker_order, taker_order, maker_exchange, taker_exchange):

    open_order[symbol_id][maker_exchange] = {

        maker_exchange + "-" + taker_exchange:{

            "maker": maker_order,
            "taker": taker_order

        }

    }

