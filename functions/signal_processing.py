import json

commission = json.load(open(r'C:\Users\Computer\Desktop\all_quant\HFT-Arbitrage\HFT-Arbitrage\config\commission.json'))

def mkt_nbbo(book_price, symbol_id):

    nbbo = {}

    MM_BEx = min(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['bid'])
    MM_AEx = max(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['ask'])
    MT_BEx = min(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['bid'])
    MT_AEx = max(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['bid'])
    TM_BEx = min(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['ask'])
    TM_AEx = max(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['ask'])
    TT_BEx = min(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['ask'])
    TT_AEx = max(book_price[symbol_id], key = lambda x: book_price[symbol_id][x]['bid'])

    '''

    return:

    'BTC-USDT-PERP': {

        'NBBOMM': {'bid_exchange': 'BINANCE_FUTURES', 
                    'ask_exchange': 'BITMEX', 
                    'nbbomm_spread': Decimal('39.50'),
                    'signal': 18.7092
                }, 

        'NBBOMT': {'bid_exchange': 'BINANCE_FUTURES', 
                    'ask_exchange': 'BYBIT', 
                    'nbbomt_spread': Decimal('34.50'),
                    'signal': 112.3092
                }, 

        'NBBOTM': {'bid_exchange': 'BINANCE_FUTURES', 
                    'ask_exchange': 'BITMEX', 
                    'nbbotm_spread': Decimal('39.49'),
                    'signal': 37.41840800000001}
                }, 

        'NBBOTT': {'bid_exchange': 'BINANCE_FUTURES', 
                    'ask_exchange': 'BYBIT', 
                    'nbbott_spread': Decimal('34.49'),
                    'signal': 131.00491300000002
                }
            }
        }

    '''

    nbbo[symbol_id] = {

        "NBBOMM": {

            "bid_exchange": MM_BEx,
            "ask_exchange": MM_AEx,
            "spread": book_price[symbol_id][MM_AEx]["ask"] - book_price[symbol_id][MM_BEx]["bid"],
            "signal": book_price[symbol_id][MM_BEx]["bid"] * commission["USDM"]["MAKER"][MM_BEx] * 2 +
                      book_price[symbol_id][MM_AEx]["ask"] * commission["USDM"]["MAKER"][MM_AEx] * 2 +
                      max(book_price[symbol_id][MM_BEx]["bid"], book_price[symbol_id][MM_AEx]["ask"]) * 0.0005

        },

        "NBBOMT": {

            "bid_exchange": MT_BEx,
            "ask_exchange": MT_AEx,
            "spread": book_price[symbol_id][MT_AEx]["bid"] - book_price[symbol_id][MT_BEx]["bid"],
            "signal": book_price[symbol_id][MT_BEx]["bid"] * commission["USDM"]["MAKER"][MT_BEx] * 2 +
                      book_price[symbol_id][MT_AEx]["bid"] * commission["USDM"]["TAKER"][MT_AEx] * 2 +
                      max(book_price[symbol_id][MT_BEx]["bid"], book_price[symbol_id][MT_AEx]["bid"]) * 0.0005
        },

        "NBBOTM": {

            "bid_exchange": TM_BEx,
            "ask_exchange": TM_AEx,
            "spread": book_price[symbol_id][TM_AEx]["ask"] - book_price[symbol_id][TM_BEx]["ask"],
            "signal": book_price[symbol_id][TM_BEx]["ask"] * commission["USDM"]["TAKER"][TM_BEx] * 2 +
                      book_price[symbol_id][TM_AEx]["ask"] * commission["USDM"]["MAKER"][TM_AEx] * 2 +
                      max(book_price[symbol_id][TM_BEx]["ask"], book_price[symbol_id][TM_AEx]["ask"]) * 0.0005
        },

        "NBBOTT": {

            "bid_exchange": TT_BEx,
            "ask_exchange": TT_AEx,
            "spread": book_price[symbol_id][TT_AEx]["bid"] - book_price[symbol_id][TT_BEx]["ask"],
            "signal": book_price[symbol_id][TT_BEx]["ask"] * commission["USDM"]["TAKER"][TT_BEx] * 2 +
                      book_price[symbol_id][TT_AEx]["bid"] * commission["USDM"]["TAKER"][TT_AEx] * 2 +
                      max(book_price[symbol_id][TT_BEx]["ask"], book_price[symbol_id][TT_BEx]["bid"]) * 0.0005

        },

    }

    return nbbo

def all_combo(symbol_id, book_price, exchange):

    combo = {}

    exchange_list = list(book_price[symbol_id].keys())
    exchange_list.remove(exchange)
    
    for exch in exchange_list:

        if book_price[symbol_id][exchange]["bid"] < book_price[symbol_id][exch]["bid"]:

            combo[exchange + "__" + exch] = {

                    "NBBOMT":{

                        "bid_exchange": exchange,
                        "ask_exchange": exch,
                        "spread": book_price[symbol_id][exch]["bid"] - book_price[symbol_id][exchange]["bid"],
                        "signal": book_price[symbol_id][exchange]["bid"] * commission["USDM"]["MAKER"][exchange] * 2 + book_price[symbol_id][exch]["bid"] * commission["USDM"]["TAKER"][exch] * 2 + max(book_price[symbol_id][exchange]["bid"], book_price[symbol_id][exch]["bid"]) * 0.0005

                    },

                    "NBBOTM":{

                        "bid_exchange": exchange,
                        "ask_exchange": exch,
                        "spread": book_price[symbol_id][exch]["ask"] - book_price[symbol_id][exchange]["ask"],
                        "signal": book_price[symbol_id][exchange]["ask"] * commission["USDM"]["TAKER"][exchange] * 2 + book_price[symbol_id][exch]["ask"] * commission["USDM"]["MAKER"][exch] * 2 + max(book_price[symbol_id][exchange]["ask"], book_price[symbol_id][exch]["ask"]) * 0.0005

                    },

                    "NBBOTT":{

                        "bid_exchange": exchange,
                        "ask_exchange": exch,
                        "spread": book_price[symbol_id][exch]["ask"] - book_price[symbol_id][exchange]["bid"],
                        "signal": book_price[symbol_id][exchange]["ask"] * commission["USDM"]["TAKER"][exchange] * 2 + book_price[symbol_id][exch]["bid"] * commission["USDM"]["TAKER"][exch] * 2 + max(book_price[symbol_id][exchange]["ask"], book_price[symbol_id][exch]["bid"]) * 0.0005

                    },
            
            }
        
        elif book_price[symbol_id][exchange]["bid"] > book_price[symbol_id][exch]["bid"]:

            combo[exchange + "__" + exch] = {
                
                "NBBOMT":{

                    "bid_exchange": exch,
                    "ask_exchange": exchange,
                    "spread": book_price[symbol_id][exchange]["bid"] - book_price[symbol_id][exch]["bid"],
                    "signal": book_price[symbol_id][exch]["bid"] * commission["USDM"]["MAKER"][exch] * 2 + book_price[symbol_id][exchange]["bid"] * commission["USDM"]["TAKER"][exchange] * 2 + max(book_price[symbol_id][exch]["bid"], book_price[symbol_id][exchange]["bid"]) * 0.0005

                },

                "NBBOTM":{

                    "bid_exchange": exch,
                    "ask_exchange": exchange,
                    "spread": book_price[symbol_id][exchange]["ask"] - book_price[symbol_id][exch]["ask"],
                    "signal": book_price[symbol_id][exch]["ask"] * commission["USDM"]["TAKER"][exch] * 2 + book_price[symbol_id][exchange]["ask"] * commission["USDM"]["MAKER"][exchange] * 2 + max(book_price[symbol_id][exch]["ask"], book_price[symbol_id][exchange]["ask"]) * 0.0005

                },

                "NBBOTT":{

                    "bid_exchange": exch,
                    "ask_exchange": exchange,
                    "spread": book_price[symbol_id][exchange]["ask"] - book_price[symbol_id][exch]["bid"],
                    "signal": book_price[symbol_id][exch]["ask"] * commission["USDM"]["TAKER"][exch] * 2 + book_price[symbol_id][exchange]["bid"] * commission["USDM"]["TAKER"][exchange] * 2 + max(book_price[symbol_id][exch]["ask"], book_price[symbol_id][exchange]["bid"]) * 0.0005
            
            }

        }

    return combo