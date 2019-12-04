from iexfinance.stocks import Stock
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import my_private_token
import pandas as pd
import random
import yaml
import time
import sys


IEX_TOKEN = my_private_token.LOCAL_IEX_TOKEN
base = 'https://cloud.iexapis.com/'


def write_console(str):
    for ch in str:
        sys.stdout.write(ch)
        time.sleep(0.055)
    print('')

# Make function for calls to Yahoo Finance
def get_adj_close(ticker, start, end):
    """
    A function that takes ticker symbols, starting period, ending period
    as arguments and returns with a Pandas DataFrame of the Adjusted Close Prices
    for the tickers from Yahoo Finance
    """
    start = start
    end = end
    info = web.DataReader(ticker, data_source='yahoo', start=start, end=end)['Adj Close']
    return pd.DataFrame(info)


def turn_file_to_object(file_name):
    """
    This function will take a text file with all symbols basic data
    and convert it into a python dictionary data structure via yaml library
    """
    with open(file_name, 'r') as file:
        data = file.read().replace('\n', '')
    all_symbols_object = yaml.load(data, Loader=yaml.FullLoader)
    return all_symbols_object


def stock_info(ticker):
    """
    This function will receive a ticker and print
    data structure with all main relevant data we will use
    """
    a = Stock(ticker, token=IEX_TOKEN)
    print("#### get_company_name() ####")
    print(a.get_company_name())

    print("\n#### get_quote() ####")
    main_data = a.get_quote()
    print(main_data)
    print(main_data['iexRealtimePrice'])

    print("\n#### get_shares_outstanding() ####")
    print(a.get_shares_outstanding())

    print("\n#### get_historical_prices() ####")
    print(a.get_historical_prices())

    print('\n')
    stat = a.get_key_stats()
    print("\n#### get_key_stats()####")
    print(stat)
    if 'peRatio' in stat:
        print("\n#### get_key_stats()['peRatio'] ####")
        print(stat['peRatio'])
    return a


def show_bollinger(ticker):
    """
    This function will calculate bolilnger band
    and display it in a graph
    """
    # Get Adjusted Closing Prices for Facebook, Tesla and Amazon between 2016-2017
    try:
        this_ticker = get_adj_close(str(ticker), '1/2/2018', '3/12/2018')
        this_ticker_info = Stock(ticker, token=IEX_TOKEN)
    except:
        return

    # Calculate 30 Day Moving Average, Std Deviation, Upper Band and Lower Band
    this_ticker['30 Day MA'] = this_ticker['Adj Close'].rolling(window=20).mean()
    this_ticker['30 Day STD'] = this_ticker['Adj Close'].rolling(window=20).std()
    this_ticker['Upper Band'] = this_ticker['30 Day MA'] + (this_ticker['30 Day STD'] * 2)
    this_ticker['Lower Band'] = this_ticker['30 Day MA'] - (this_ticker['30 Day STD'] * 2)

    # Simple 30 Day Bollinger Band for Facebook (2016-2017)
    this_ticker[['Adj Close', '30 Day MA', 'Upper Band', 'Lower Band']].plot(figsize=(12, 6))
    plt.title('30 Day Bollinger Band for ' + this_ticker_info.get_company_name())
    plt.ylabel('Price (USD)')
    plt.show();


def scan_symbols(n):
    chosen_symbols = []
    all_symbols_object = turn_file_to_object('all_symbols')
    random.shuffle(all_symbols_object)
    for ticker in all_symbols_object:
        if n == 0:
            random.shuffle(chosen_symbols)
            return chosen_symbols
        # return list of tuples that contain (symbol, company name)
        chosen_symbols.append((ticker['symbol'], ticker['name']))
        n -= 1


def get_sorted_swing_stocks(amount):
    i = 0
    recommended_stocks = []
    random_stocks = scan_symbols(300)
    for tick in random_stocks:
        a = Stock(tick[0], token=IEX_TOKEN)
        stat = a.get_key_stats()
        quote = a.get_quote()
        add_to_list = 0
        last_price = quote['latestPrice']
        # Avoid penny stocks
        try:
            if len(recommended_stocks) == amount:
                break
            if last_price < 5:
                continue
            # Avoid current price > week52High
            if last_price < float(quote['week52High']) - (float(last_price/10)):
                add_to_list = add_to_list + 1
            # Avoid current price < week52Low
            if last_price > quote['week52Low'] - (last_price / 10):
                add_to_list = add_to_list + 1
            # Trade Avg. Volume VS current Volume
            if quote['previousVolume'] > stat['avg30Volume']:
                add_to_list = add_to_list + 1
            # 50 day Bollinger Band
            if last_price < stat['day50MovingAvg']:
                add_to_list = add_to_list + 1
            if add_to_list == 4:
                recommended_stocks.append(tick)
                print('Added ' + str(tick[0]) + ' to recommended stocks')
                i = i + 1
            if i == amount:
                return recommended_stocks
        except KeyError as e:
            continue
        except TypeError as e:
            continue
        except iexfinance.utils as e:
            continue


def get_sorted_value_stocks(amount):
    i = 0
    recommended_stocks = []
    random_stocks = scan_symbols(300)
    for tick in random_stocks:
        a = Stock(tick[0], token=IEX_TOKEN)
        stat = a.get_key_stats()
        quote = a.get_quote()
        add_to_list = 0
        last_price = quote['latestPrice']
        # Avoid penny stocks
        try:
            if len(recommended_stocks) == amount:
                break
            if last_price < 5:
                continue
            # Avoid current price > week52High
            if last_price < float(quote['week52High']) - (float(last_price / 10)):
                add_to_list = add_to_list + 1
            # Avoid current price < week52Low
            if last_price > quote['week52Low'] - (last_price / 10):
                add_to_list = add_to_list + 1
            # Trade Avg. Volume VS current Volume
            if quote['previousVolume'] > stat['avg30Volume']:
                add_to_list = add_to_list + 1
            # low P/E ratio
            if stat['peRatio'] < 15:
                add_to_list = add_to_list + 1
            if add_to_list == 4:
                recommended_stocks.append(tick)
                print('Added ' + str(tick[0]) + ' to recommended stocks')
                i = i + 1
            if i == amount:
                return recommended_stocks
        except KeyError as e:
            continue
        except TypeError as e:
            continue
        except iexfinance.utils as e:
            continue


def get_recommended_stocks(choice, num):
    if choice == 1:
        recommended_symbols = get_sorted_swing_stocks(num)
    if choice == 2:
        recommended_symbols = get_sorted_value_stocks(num)

    return recommended_symbols


def create_title(str, ch):
    return ''.ljust(len(str), ch) + '\n' + str + '\n' + ''.ljust(len(str), ch)