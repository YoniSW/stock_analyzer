from iexfinance.stocks import get_historical_data
from pandas_datareader import data
from iexfinance.stocks import get_historical_intraday
from iexfinance.altdata import get_social_sentiment
from iexfinance.stocks import Stock
from datetime import datetime
from stock_functions import *
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import my_private_token
import yaml
import os
import pandas as pd
import csv
import pyEX as p

# Do not embed API keys directly in code - security
IEX_TOKEN = my_private_token.LOCAL_IEX_TOKEN
base = 'https://cloud.iexapis.com/'


def main():
    print('\n')
    print(create_title('Welcome to STOCK ANALYZER', '$'))
    # print('which value investor are you?')
    # print('For swing investment - click 1')
    # print('For value investment - click 2')
    # choice = input('')
    # print('How many recommended stocks do want to receive?')
    # num_of_stocks = input('')

    # DEBUG vars
    #################
    choice = 1
    num_of_stocks = 5
    #################

    recommended_stocks = get_recommended_stocks(choice, num_of_stocks)
    print(recommended_stocks)

    # for s in recommended_stocks:
    #     show_bollinger(s)

    # stock_info('fb')
    # show_bollinger('teva')


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    print('\n\nExecution time: ' + str(datetime.now() - start_time) + 'ms')