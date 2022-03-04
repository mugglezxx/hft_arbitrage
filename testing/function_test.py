book_price = {'BTCUSDPERP': {
    'OKEX': {'receipt_timestamp': 1644895124.1799657, 'bid': 43593.2, 'ask': 43593.3, 'bid_size': 1597.0, 'ask_size': 277.0},
    'BYBIT': {'receipt_timestamp': 1644895126.2072468, 'bid': 43549.5, 'ask': 43550.0, 'bid_size': 79.869, 'ask_size': 2.15},
    'BINANCE_FUTURES': {'receipt_timestamp': 1644895124.4852324, 'bid': 43579.99, 'ask': 43580.0, 'bid_size': 1.461, 'ask_size': 0.151},
    'FTX': {'receipt_timestamp': 1644895124.3473113, 'bid': 43646.0, 'ask': 43647.0, 'bid_size': 3.3925, 'ask_size': 0.8245},
    'DYDX': {'receipt_timestamp': 1644895125.8764365, 'bid': 43631.0, 'ask': 43633.0, 'bid_size': 10.2561, 'ask_size': 1.5153},
    'BITFINEX': {'receipt_timestamp': 1644895124.013061, 'bid': 43623.0, 'ask': 43631.0, 'bid_size': 0.28055023, 'ask_size': 0.14584635},
    'BITMEX': {'receipt_timestamp': 1644895126.087316, 'bid': 43598.5, 'ask': 43606.0, 'bid_size': 350000.0, 'ask_size': 350000.0}
    }
}

trade_record = {'BTCUSDPERP': {
    'BINANCE_FUTURES': {'receipt_timestamp': 1644895124.4832337, 'exchange': 'BINANCE_FUTURES', 'symbol': 'BTC-USDT-PERP', 'side': 'buy', 'price': 43580.00, 'amount': 0.206},
    'OKEX': {'receipt_timestamp': 1644895113.935924, 'exchange': 'OKEX', 'symbol': 'BTC-USDT-PERP', 'side': 'sell', 'price': 43593.2, 'amount': 2},
    'BYBIT': {'receipt_timestamp': 1644895126.2142434, 'exchange': 'BYBIT', 'symbol': 'BTC-USDT-PERP', 'side': 'sell', 'price': 43000.00, 'amount': 0.004},
    'BITFINEX': {'receipt_timestamp': 1644895123.2924736, 'exchange': 'BITFINEX', 'symbol': 'BTC-USDT-PERP', 'side': 'buy', 'price': 43618, 'amount': 0.001},
    'DYDX': {'receipt_timestamp': 1644895125.725523, 'exchange': 'DYDX', 'symbol': 'BTC-USD-PERP', 'side': 'buy', 'price': 43634, 'amount': 0.3},
    'FTX': {'receipt_timestamp': 1644895114.8119338, 'exchange': 'FTX', 'symbol': 'BTC-USD-PERP', 'side': 'buy', 'price': 43645.0, 'amount': 0.1},
    'BITMEX': {'receipt_timestamp': 1644895105.8126752, 'exchange': 'BITMEX', 'symbol': 'BTC-USDT-PERP', 'side': 'buy', 'price': 43569, 'amount': 3000}
    }
}

nbbo_book = {'BTCUSDPERP': {
    'NBBOMM': {'bid_exchange': 'BYBIT', 'ask_exchange': 'FTX', 'spread': 97.5, 'signal': 17.50755},
    'NBBOMT': {'bid_exchange': 'BINANCE_FUTURES', 'ask_exchange': 'FTX', 'spread': 96.5, 'signal': 17.50665},
    'NBBOTM': {'bid_exchange': 'BYBIT', 'ask_exchange': 'FTX', 'spread': 97.0, 'signal': 104.6073},
    'NBBOTT': {'bid_exchange': 'BYBIT', 'ask_exchange': 'FTX', 'spread': 200, 'signal': 104.5584}
    }
}

symbols = ["BTCUSDPERP", "ETHUSDPERP", "SOLUSDPERP"]

#orders = {symbol: {} for symbol in symbols}

import functions.op_management as opm
import functions.order_processing as op
import functions.record_management as rm
import functions.signal_processing as sp
import functions.trade_processing as tp

exchange_id = "BYBIT"
symbol_id = symbols[0]
order, maker_exchange, taker_exchange = op.tm_order(symbol_id, book_price, nbbo_book)

orders["BTCUSDPERP"] = {

    maker_exchange:{

        maker_exchange + taker_exchange: {

            "maker": order[symbol_id]["buy_order"],
            "taker": order[symbol_id]["sell_order"]

        }

    }

}


