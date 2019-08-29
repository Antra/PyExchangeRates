import requests
import json
import time

# Some basics
exchange_rate_url = 'http://api.openrates.io/latest'
companies = {'NG': '',
             'NG100': 'EUR',
             'NG200': 'USD',
             'NG300': 'GBP',
             'NG400': 'NOK',
             'NG500': 'SEK',
             'NG600': 'JPY',
             'NG700': 'MXN'}
#date = ''
currencies = set(filter(None, companies.values()))


def get_reverse_rate(rate):
    return 1 / rate


def get_currency(currency):
    request_url = exchange_rate_url + '?base=' + currency
    response = requests.get(request_url)
    date = response.json()['date']
    return response.json()['rates'], date


responses = {}

for currency in currencies:

    responses[currency], responses[currency]['date'] = get_currency(currency)
    time.sleep(1)

# Just EUR
print(responses['EUR'])
# Just EUR -> CAD rate
print(responses['EUR']['CAD'])
# Just EUR -> CAD rate (reverse)
print(get_reverse_rate(responses['EUR']['CAD']))
# Just all the currencies relating to EUR
print(responses['EUR'].keys())

for key, value in responses['EUR'].items():
    if key != 'date':
        print("currency " + key + " has exchange rate " +
              str(value) + " against EUR\n")
        print("currency " + key + " has exchange rate " +
              str(get_reverse_rate(value)) + " against EUR (reversed)\n")

# Did we get the date as well? We should have
print(responses['EUR']['date'])
print(responses['JPY']['date'])


def generate_currency_pair(currency1, currency2, rate):
    pass


# How do I actually generate a file?
# for currency in currencies
#     for currency2 in responses[currency].keys()
#           curr_pair_list = generate_currency_pair(currency, currency2, responses[currency][currency2])
#           valid_from = date
#           companies = get_companies(currency)
