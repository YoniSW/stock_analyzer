from pandas_datareader import data
from iexfinance.stocks import Stock
from datetime import datetime
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import get_historical_intraday

IEX_TOKEN = 'pk_e26954db0aca40eabd7947fe39d03281'
a = Stock("BAC", token=IEX_TOKEN)
print("#### Stock Official name ####")
print(a.get_company_name())

print("\n#### Stock Main Data ####")
print(a.get_quote())

print("\n#### Stock last dividend ####")
print(a.get_dividends())

print("\n#### Stock historical prices ####")
print(a.get_historical_prices())



#
# start_date = '2005-01-01'
# end_date = '2019-12-30'
#
# start = datetime(2016, 1, 1)
end = datetime(2019, 1, 1)
# # User pandas_reader.data.DataReader to load the desired data. As simple as that.
# panel_data = data.DataReader('INPX', 'iex', start, end, api_key="pk_e26954db0aca40eabd7947fe39d03281")
# print(panel_data)
# tsla = Stock('TSLA', token=IEX_TOKEN)
# print(tsla.get_price())
