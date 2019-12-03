from iexfinance.stocks import Stock
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import my_private_token
import yaml
import pandas as pd


IEX_TOKEN = my_private_token.LOCAL_IEX_TOKEN
base = 'https://cloud.iexapis.com/'

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
    this_ticker = get_adj_close(str(ticker), '1/2/2016', '31/12/2017')
    this_ticker_info = stock_info(ticker)

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
    for ticker in all_symbols_object:
        if n == 0:
            return chosen_symbols
        # return list of tuples that contain (symbol, company name)
        chosen_symbols.append((ticker['symbol'], ticker['name']))
        n -= 1


def get_sorted_swing_stocks(amount):
    """
    -Trade Avg. Volume VS current Volume
    -50 day Bollinger Band
    -52 Week price Range
    -Weekly price range
    -Daily price Range
    -Avoid ‘penny’ stocks
    """
    random_stocks = scan_symbols(amount)
    for stock in random_stocks:
        tick = stock[0]
        print(tick)
        if tick.get_company_name()['latestVolume'] > tick.get_key_stats()['avg30Volume']:
            print(stock)


def get_sorted_value_stocks(amount):
    """
     -Low p/e ratio according to sector
     -Profitable stocks
     -Avoid ‘penny’ stocks
     """
    random_stocks = scan_symbols(amount)


def get_recommended_stocks(choice, num):
    if choice == 1:
        recommended_symbols = get_sorted_swing_stocks(num)
    if choice == 2:
        recommended_symbols = get_sorted_value_stocks(num)

    return recommended_symbols


def create_title(str, ch):
    return ''.ljust(len(str), ch) + '\n' + str + '\n' + ''.ljust(len(str), ch)