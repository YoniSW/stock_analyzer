from iexfinance.stocks import get_historical_data
from pandas_datareader import data
from iexfinance.stocks import get_historical_intraday
from iexfinance.altdata import get_social_sentiment
from iexfinance.stocks import Stock
from datetime import datetime
import matplotlib.pyplot as plt
import my_private_token
import requests
import yaml
import json
import os
import pandas
import csv
import pyEX as p


# Make function for calls to Yahoo Finance
def get_adj_close(ticker, start, end):
    '''
    A function that takes ticker symbols, starting period, ending period
    as arguments and returns with a Pandas DataFrame of the Adjusted Close Prices
    for the tickers from Yahoo Finance
    '''
    start = start
    end = end
    info = web.DataReader(ticker, data_source='yahoo', start=start, end=end)['Adj Close']
    return pd.DataFrame(info)

# Get Adjusted Closing Prices for Facebook, Tesla and Amazon between 2016-2017
fb = get_adj_close('fb', '1/2/2016', '31/12/2017')
tesla = get_adj_close('tsla', '1/2/2016', '31/12/2017')
amazon = get_adj_close('amzn', '1/2/2016', '31/12/2017')

# Calculate 30 Day Moving Average, Std Deviation, Upper Band and Lower Band
for item in (fb, tesla, amazon):
    item['30 Day MA'] = item['Adj Close'].rolling(window=20).mean()
    item['30 Day STD'] = item['Adj Close'].rolling(window=20).std()
    item['Upper Band'] = item['30 Day MA'] + (item['30 Day STD'] * 2)
    item['Lower Band'] = item['30 Day MA'] - (item['30 Day STD'] * 2)

# Simple 30 Day Bollinger Band for Facebook (2016-2017)
fb[['Adj Close', '30 Day MA', 'Upper Band', 'Lower Band']].plot(figsize=(12,6))
plt.title('30 Day Bollinger Band for Facebook')
plt.ylabel('Price (USD)')
plt.show();


# Do not embed API keys directly in code - security
IEX_TOKEN = my_private_token.LOCAL_IEX_TOKEN
base = 'https://cloud.iexapis.com/'


def turn_file_to_object(file_name):
    with open(file_name, 'r') as file:
        data = file.read().replace('\n', '')
    all_symbols_object = yaml.load(data, Loader=yaml.FullLoader)
    return all_symbols_object


def activate_single_stock(ticker):
    a = Stock(ticker, token=IEX_TOKEN)
    print("#### Stock Official name ####")
    print(a.get_company_name())

    print("\n#### Stock Main Data ####")
    main_data = a.get_quote()
    print(main_data)
    print(main_data['iexRealtimePrice'])

    print("\n#### Stock shares outstanding ####")
    print(a.get_shares_outstanding())

    print("\n#### Stock historical prices ####")
    print(a.get_historical_prices())

    print('\n')
    stat = a.get_key_stats()
    print(stat)
    if 'peRatio' in stat:
        print(stat['peRatio'])


def main():
    # print('which value investor are you?')
    # print('For daily investment - click 1')
    # print('For swing investment - click 2')
    # print('For value investment - click 3')
    # choice = input('')

    #####  send single stock to function
    # activate_single_stock('TEVA')

    all_symbols_object = turn_file_to_object('all_symbols')
    print(type(all_symbols_object))
    print(type(all_symbols_object[1]))

    for ticker in all_symbols_object:
        print(ticker['symbol'])

    print('\nNumber of tickers: ' + str(len(all_symbols_object)))

    # plt.plot([1, 2, 3, 4, 5, 8])
    # plt.ylabel('some numbers')
    # plt.show()


    #####  optional functions

    # start = datetime(2019, 1, 1)
    # end = datetime(2019, 10, 10)
    # # # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    # panel_data = data.DataReader('DAL', 'iex', start, end, api_key=IEX_TOKEN)
    # print(panel_data)
    # # symbols = requests.get(base + 'beta/ref-data/symbols?token=pk_e26954db0aca40eabd7947fe39d03281')
    # # data = symbols.json()
    # # print(symbols)
    # # Check

if __name__ == '__main__':
    start_time = datetime.now()
    main()
    print('\n\nExecution time: ' + str(datetime.now() - start_time) + 'ms')