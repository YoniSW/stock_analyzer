from iexfinance.stocks import get_historical_data
from pandas_datareader import data
from iexfinance.stocks import get_historical_intraday
from iexfinance.altdata import get_social_sentiment
from iexfinance.stocks import Stock
from datetime import datetime
import my_private_token
import requests
import yaml
import json
import os
import pandas
import csv
import pyEX as p


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

    # activate_single_stock('TEVA')
    # start = datetime(2019, 1, 1)
    # end = datetime(2019, 10, 10)
    # # # User pandas_reader.data.DataReader to load the desired data. As simple as that.
    # panel_data = data.DataReader('DAL', 'iex', start, end, api_key=IEX_TOKEN)
    # print(panel_data)
    # symbols = requests.get('https://cloud.iexapis.com/beta/ref-data/symbols?token=pk_e26954db0aca40eabd7947fe39d03281')
    # data = symbols.json()
    # print(symbols)

    all_symbols_object = turn_file_to_object('all_symbols')
    print(type(all_symbols_object))
    print(type(all_symbols_object[1]))


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    print('\n\nExecution time: ' + str(datetime.now() - start_time) + 'ms')