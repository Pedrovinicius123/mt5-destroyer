from dotenv import load_dotenv
from datetime import datetime
from src.core import init
from time import sleep
from random import uniform

import MetaTrader5 as mt5
import pandas as pd
import numpy as np

import pickle
import os


def intervals(intervs):
    """
    Function to process intervals and return a result based on calculations.

    Parameters:
    intervs (list): A list of intervals.

    Returns:
    dict or None: A dictionary with 'code' and 'closeLog' keys if sumUp is greater than sumDown or less than sumDown respectively. Returns None if sumUp is equal to sumDown.

    """

    up = []
    lower = []
    print('Intervals: ', intervs)

    ceil = uniform(6, 7)
    floor = uniform(5, 6)

    counter_up = 0
    counter_down = 0

    uppers = np.array([])
    lowers = np.array([])

    closeLog = []

    for i in intervs:
        i = list(map(lambda num: round(num), i))

        for idx in range(sorted(i)[0], sorted(i)[1] + 1):
            sortedArr = sorted(i)
            closeLog.append(sortedArr[1])

            result = init(idx)

            if result['up'] > result['down']:
                counter_up += 1
            else:
                counter_down += 1

            up.append(result['up'])
            lower.append(result['down'])

    print('Up: ', len(up))
    print('Down: ', len(lower))
    i = 0
    index = list(map(lambda n: i, closeLog))
    indexStr = list(map(lambda n: 'a', closeLog))
    indexStr = ''.join(indexStr)

    sumUp = sum(up) / ceil
    sumDown = sum(lower) / floor

    print(sumDown)
    print(sumUp)

    if sumUp > sumDown:
        return {'code': True, 'closeLog': closeLog[index[-1]], 'ceil': ceil, 'floor': floor}
    elif sumUp == sumDown:
        return None
    else:
        return {'code': False, 'closeLog': closeLog[index[-1]], 'ceil': ceil}


load_dotenv()

login = int(os.environ['LOGIN'])
password = os.environ['PASSWORD']
svr = os.environ['SVR']

print(svr)


def make_money_for_me(times):
    for i in range(times):

        auth = mt5.initialize(
            "/home/pedro/.wine/dosdevices/c:/Program Files/MetaTrader 5/terminal64.exe", login=login,
            server=svr,
            password=password
        )

        if auth:

            print('Conn successful')

            # Getting data

            symbol = 'GBPUSD'
            number_of_data = 1000
            timeframe = mt5.TIMEFRAME_M1
            from_date = datetime.now()

            data = mt5.copy_rates_from(symbol, timeframe, from_date, number_of_data)

            # Shaping data
            df_rates = pd.DataFrame(data)
            df_rates['time'] = pd.to_datetime(df_rates['time'], unit='s')

            df_rates['open'] = df_rates['open'] * 10 ** 1
            df_rates['close'] = df_rates['close'] * 10 ** 1
            high = df_rates['open'].to_list()
            low = df_rates['close'].to_list()

            arr = np.stack((high, low), axis=1)

            # Applying algorithm

            result = intervals(arr)

            print(result['code'])
            sleep(2)

            if result['code']:
                order = mt5.ORDER_TYPE_BUY
                price = mt5.symbol_info_tick(symbol).ask

            else:
                order = mt5.ORDER_TYPE_SELL
                price = mt5.symbol_info_tick(symbol).bid

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": 0.01,
                "type": order,
                "price": price,
                "type_time": mt5.ORDER_TIME_GTC,
            }

            order_sent = mt5.order_send(request)

            print(order_sent)
            profit = 0
            counter = 0

            ticket = None

            def get_profit(order_snt=None):
                try:

                    pos = mt5.positions_get(symbol=symbol)
                    print(pos)

                    order_snt = pos[0]

                except Exception as err_0:
                    print(err_0)
                    mt5.shutdown()

                else:
                    pass

                ticket = order_snt.ticket
                money = float(order_snt.profit)

                return money, ticket

            while True:
                profit = get_profit()

                print(profit[0])

                if profit[0] >= 0.2 or profit[0] <= -0.2:

                    if profit[0] > 0:
                        print('Win! :D')
                        resultado = 1

                    else:
                        print('Loss ;-;')
                        resultado = 0

                    break

                counter += 0.1

                if counter > 60 * 7 - 1:
                    if profit[0] < 0:
                        print('Lose ;-;')
                        resultado = 0

                    else:
                        print('Win! :D')
                        resultado = 1

                    break

                sleep(0.1)

            mt5.Close(symbol, ticket=profit[1])

            mt5.shutdown()

            return resultado, result['ceil'], result['floor']

        else:
            print(f'Error: {mt5.last_error()}')
            mt5.shutdown()

arr_results = np.array([])
arr_lowers = np.array([])
arr_uppers = np.array([])

while True:

    try:
        with open('results.pkl', 'rb') as file_read:
            arr_results = pickle.load(file_read)

        with open('uppers.pkl', 'rb') as file_read_0:
            arr_uppers = pickle.load(file_read_0)

        with open('lowers.pkl', 'rb') as file_read_1:
            arr_lowers = pickle.load(file_read_1)

    except Exception:
        print("File not created yet")

    res = make_money_for_me(1)

    arr_results = np.append(arr_results, res[0])
    arr_uppers = np.append(arr_uppers, res[1])
    arr_lowers = np.append(arr_lowers, res[2])

    with open('results.pkl', 'wb') as file:
        pickle.dump(arr_results, file)

    with open('uppers.pkl', 'wb') as file:
        pickle.dump(arr_uppers, file)

    with open('lowers.pkl', 'wb') as file:
        pickle.dump(arr_lowers, file)

    sleep(1)
