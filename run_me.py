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
    print('')
    choice = input('')
    write_console('How many recommended stocks do want to receive?')
    num_of_stocks = input('')
    write_console('\nScanning all USA Stock Market, It may take a while...')
    recommended_stocks = get_recommended_stocks(int(choice), int(num_of_stocks))
    write_console('\n\nDone scanning your stocks!\n')
    print(''.ljust(75, '='))
    for s in recommended_stocks:
        print('|' + str(s[0]).ljust(10) + '|' + str(s[1]).ljust(62) + '|')
    print(''.ljust(75, '='))
    write_console('\n\nSystem will show bollinger bands forthose stocks\n')
    for s in recommended_stocks:
        show_bollinger(s[0])
        time.sleep(1)


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    print('\n\nExecution time: ' + str(datetime.now() - start_time) + 'ms')