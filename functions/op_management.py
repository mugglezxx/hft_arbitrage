import redis
import json
import ast

db_keys = json.load(open(r'C:\Users\Computer\Desktop\all_quant\HFT-Arbitrage\HFT-Arbitrage\config\database_key.json'))
mt_order_database = redis.Redis(host = db_keys["redis"]["host"], port = db_keys["redis"]["port"], db = 0)
tm_order_database = redis.Redis(host = db_keys["redis"]["host"], port = db_keys["redis"]["port"], db = 1)
sorder_database = redis.Redis(host = db_keys["redis"]["host"], port = db_keys["redis"]["port"], db = 2)
position_database = redis.Redis(host = db_keys["redis"]["host"], port = db_keys["redis"]["port"], db = 3)
sposition_database = redis.Redis(host = db_keys["redis"]["host"], port = db_keys["redis"]["port"], db = 4)

def mt_orders(symbol_id, order_dict):

    mt_order_database.hmset(symbol_id, order_dict)

def tm_orders(symbol_id, order_dict):

    tm_order_database.hmset(symbol_id, order_dict)

def open_positions(symbol_id, trade, exchange):

    traded = trade[symbol_id]

    if position_database.hexists(exchange, symbol_id):

        exist_position = position_database.hmget(exchange, symbol_id)
        open_p = ast.literal_eval(exist_position[0].decode("utf-8"))

        price = (open_p["price"] * open_p["amount"] + traded["trade_price"] * traded["trade_amount"]) / (open_p["amount"] + traded["trade_amount"])
        amount = (open_p["amount"] + traded["trade_amount"])
        side = traded["side"]

        new_position = {

            symbol_id: {

                "symbol": symbol_id,
                "exchange": exchange,
                "side": side,
                "price": price,
                "amount": amount

            }

        }

        position_database.hmset(exchange, new_position)

    else:

        new_position = {

            symbol_id: {

                "symbol": symbol_id,
                "exchange": traded["exchange"],
                "side": traded["side"],
                "price": traded["trade_price"],
                "amount": traded["trade_amount"]

            }

        }

        position_database.hmset(exchange, new_position)

def open_spositions(symbol_id, maker_trade, taker_trade, maker_exchange, taker_exchange):

    leg1_traded = maker_trade[symbol_id]
    leg2_traded = taker_trade[symbol_id]

    if sposition_database.hexists(maker_exchange + "__" + taker_exchange, symbol_id) == True:

        exist_position = sposition_database.hmget(maker_exchange + "__" + taker_exchange, symbol_id)
        open_p = ast.literal_eval(exist_position[0].decode("utf-8"))
        leg1_side = leg1_traded["side"]
        leg2_side = leg2_traded["side"]
        leg1_price = (leg1_traded["trade_price"] * leg1_traded["trade_amount"]) + (open_p["leg1_price"] * open_p["leg1_amount"]) / (leg1_traded["trade_amount"] + open_p["leg1_amount"])
        leg2_price = (leg2_traded["trade_price"] * leg2_traded["trade_amount"]) + (open_p["leg2_price"] * open_p["leg2_amount"]) / (leg2_traded["trade_amount"] + open_p["leg2_amount"])
        leg1_amount = leg1_traded["trade_amount"] + open_p["leg1_amount"]
        leg2_amount = leg2_traded["trade_amount"] + open_p["leg2_amount"]

        new_position = {

            symbol_id: {

                "symbol_id": symbol_id,
                "maker_exchange": leg1_traded["exchange"],
                "taker_exchange": leg2_traded["exchange"],
                "leg1_exchange": leg1_traded["exchange"],
                "leg2_exchange": leg2_traded["exchange"],
                "leg1_side": leg1_side,
                "leg2_side": leg2_side,
                "leg1_price": leg1_price,
                "leg2_price": leg2_price,        
                "leg1_amount": leg1_amount,
                "leg2_amount": leg2_amount,

            }

        }

        sposition_database.hmset(maker_exchange + "__" + taker_exchange, new_position)

    else:

        new_position = {

            symbol_id: {

                "symbol_id": symbol_id,
                "maker_exchange": leg1_traded["exchange"],
                "taker_exchange": leg2_traded["exchange"],
                "leg1_exchange": leg1_traded["exchange"],
                "leg2_exchange": leg2_traded["exchange"],
                "leg1_side": leg1_traded["side"],
                "leg2_side": leg2_traded["side"],
                "leg1_price": leg1_traded["trade_price"],
                "leg2_price": leg2_traded["trade_price"],        
                "leg1_amount": leg1_traded["trade_amount"],
                "leg2_amount": leg2_traded["trade_amount"],

            }

        }

        sposition_database.hmset(maker_exchange + "__" + taker_exchange, new_position)

def open_positions_delete(exchange, symbol_id):

    position_database.hdel(exchange, symbol_id)

def strat_positions_delete(exchange, symbol_id):

    sposition_database.hdel(exchange, symbol_id)

def mtorder_update(symbol_id, max_pair, exchange):

    maker_exchange = exchange.encode()

    all_order = mt_order_database.hgetall(symbol_id)
    maker_redis = ast.literal_eval(maker_exchange.decode("utf-8"))
    maker_redis.pop(max_pair)
    all_order[maker_exchange] = maker_redis

    mt_order_database.hmset(symbol_id, all_order)

def tmorder_update(symbol_id, min_pair, exchange):

    maker_exchange = exchange.encode()

    all_order = mt_order_database.hgetall(symbol_id)
    maker_redis = ast.literal_eval(maker_exchange.decode("utf-8"))
    maker_redis.pop(min_pair)
    all_order[maker_exchange] = maker_redis

    mt_order_database.hmset(symbol_id, all_order)