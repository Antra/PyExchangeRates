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

currencies = set(filter(None, companies.values()))


def get_reverse_rate(rate):
    return 1 / rate


def get_currency(currency):
    request_url = exchange_rate_url + '?base=' + currency
    response = requests.get(request_url)
    return response.json()['rates']


responses = {}

for currency in currencies:

    responses[currency] = get_currency(currency)
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
    print("currency " + key + " has exchange rate " +
          str(value) + " against EUR\n")
    print("currency " + key + " has exchange rate " +
          str(get_reverse_rate(value)) + " against EUR (reversed)\n")
