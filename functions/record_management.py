from qpython import qconnection
import time

q = qconnection.QConnection(host = "localhost", port = 5002, pandas = True)

q.open()

q.sendSync("""trades:([]order_time: `float$();
                        receipt_time: `float$();
                        trade_time: `float$();
                        symbol: `symbol$();
                        exchange: `symbol$();
                        order_type: `symbol$();
                        side: `symbol$();
                        order_price: `float$();
                        order_amount: `float$();
                        total_order_value: `float$();
                        trade_price: `float$();
                        trade_amount: `float$();
                        total_trade_value: `float$();
                        strategy: `symbol$();
                        status: `symbol$();
                        profit: `float$())""")

q.sendSync("""orders:([]order_time: `float$();
                        receipt_time: `float$();
                        symbol: `symbol$();
                        exchange: `symbol$();
                        order_type: `symbol$();
                        side: `symbol$();
                        order_price: `float$();
                        order_amount: `float$();
                        total_order_value: `float$();
                        strategy: `symbol$();
                        status: `symbol$())""")

def q_new_order(symbol_id, order, exchange, status):

    q.sendSync('`orders insert({};{};`{};`{};`{};`{};{};{};{};`{};`{})'.format(

        order["order_time"],
        order["receipt_time"],
        symbol_id,
        exchange,
        order["type"],
        order["side"],
        order["price"],
        order["amount"],
        order["price"] * order["amount"],
        order["strategy"],
        status

    ))

def q_new_trade(symbol_id, trade, status):

    all_trade = trade[symbol_id]

    q.sendSync('`trades insert({};{};{};`{};`{};`{};`{};{};{};{};{};{};{};`{};`{};{})'.format(
        all_trade["order_time"],
        all_trade["receipt_time"],
        all_trade["trade_time"],
        all_trade["symbol"],
        all_trade["exchange"],
        all_trade["type"],
        all_trade["side"],
        all_trade["order_price"],
        all_trade["order_amount"],
        all_trade["total_order_value"],
        all_trade["trade_price"],
        all_trade["trade_amount"],
        all_trade["total_trade_value"],
        all_trade["strategy"],
        status,
        float(0)

    ))

def q_close_trade(symbol_id, position, exchange, trade, status):

    pos = position[exchange][symbol_id]

    all_trade = trade[symbol_id]

    q.sendSync('`trades insert({};{};{};`{};`{};`{};`{};{};{};{};{};{};{};`{};`{};{})'.format(
        all_trade["order_time"],
        all_trade["receipt_time"],
        all_trade["trade_time"],
        all_trade["symbol"],
        all_trade["exchange"],
        all_trade["type"],
        all_trade["side"],
        all_trade["order_price"],
        all_trade["order_amount"],
        all_trade["total_order_value"],
        all_trade["trade_price"],
        all_trade["trade_amount"],
        all_trade["total_trade_value"],
        all_trade["strategy"],
        status,
        (all_trade["trade_price"] * all_trade["trade_amount"]) - (pos["price"] * all_trade["trade_amount"])

    ))