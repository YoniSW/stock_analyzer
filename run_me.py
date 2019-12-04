from datetime import datetime
from stock_functions import *
import my_private_token
import time

# Do not embed API keys directly in code - security
IEX_TOKEN = my_private_token.LOCAL_IEX_TOKEN
base = 'https://cloud.iexapis.com/'


def main():
    print('\n')
    print(create_title('Welcome to STOCK ANALYZER', '$'))
    write_console('\nWhich value investor are you?')
    write_console('For swing investment - click 1')
    write_console('For value investment - click 2')
    choice = input('')
    write_console('How many recommended stocks do want to receive?')
    num_of_stocks = input('')
    write_console('\nScanning all USA Stock Market, It may take a while...')
    recommended_stocks = get_recommended_stocks(int(choice), int(num_of_stocks))
    print(recommended_stocks)

    for s in recommended_stocks:
        show_bollinger(s[0])
        time.sleep(1)
    # stock_info('fb')
    # show_bollinger('teva')


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    print('\n\nExecution time: ' + str(datetime.now() - start_time) + 'ms')