import requests
import json
from datetime import datetime
import time
import uuid
import os
import logging


# setup logging
if not os.path.exists('logs'):
    os.mkdir('logs')
logging.basicConfig(filename='logs/rates.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
                    level=logging.INFO)
logging.info('PyExchangeRates starting!')


# Configuration section - update companies and auth to your setup.
companies = {'NG': '',
             'NG100': 'EUR',
             'NG200': 'USD',
             'NG300': 'GBP',
             'NG400': 'NOK',
             'NG500': 'SEK',
             'NG600': 'JPY',
             'NG700': 'MXN'}
# add API username and password inside the single-quotes below, e.g.: auth = ('api-user', 'secret-password')
auth = ('user', 'pass')


# Some constants for the functions
exchange_rate_url = 'https://api.exchangeratesapi.io/latest'
basware_exchange_rate_url = 'https://test-api.basware.com/v1/exchangeRates'
currencies = set(filter(None, companies.values()))


def add_timestamps(list):
    index = 0
    while index < len(list):
        list[index]['lastUpdated'] = str(datetime.utcnow())
        index += 1
    return list


def get_reverse_rate(rate):
    return 1 / rate


def get_api_rates(currency):
    request_url = exchange_rate_url + '?base=' + currency
    response = requests.get(request_url)
    date = response.json()['date']
    return response.json()['rates'], date


def post_api_rates(json):
    response = requests.post(basware_exchange_rate_url, auth=auth, json=json)
    return response


def get_companies_by_currency(currency):
    companylist = []
    for key, value in companies.items():
        if value == currency:
            companylist.append(key)
    return companylist


def generate_currency_pair(currency1, currency2, companies, rate, date):
    currency_pair = {}
    currency_pair_reverse = {}
    company_list = []

    # generate the array of company codes
    for company in companies:
        company_list.append(dict({"companyCode": company,
                                  "active": True}))

    # generate the 'forward' exchange rate (we get the reverse rate from the API); currency2 -> currency1 (base)
    currency_pair['rate'] = get_reverse_rate(rate)
    currency_pair['currencyCodeTo'] = currency1
    currency_pair['currencyCodeFrom'] = currency2
    currency_pair['validFrom'] = date
    currency_pair['companies'] = company_list
    currency_pair['externalCode'] = str(uuid.uuid4())
    currency_pair['lastUpdated'] = ''
    # generate the 'reverse' exchange rate (which we get from the API); currency1 (base) -> currency2
    currency_pair_reverse['rate'] = rate
    currency_pair_reverse['currencyCodeTo'] = currency2
    currency_pair_reverse['currencyCodeFrom'] = currency1
    currency_pair_reverse['validFrom'] = date
    currency_pair_reverse['companies'] = company_list
    currency_pair_reverse['externalCode'] = str(uuid.uuid4())
    currency_pair_reverse['lastUpdated'] = ''
    # return the currency pairs as a list to make life easier
    return [currency_pair, currency_pair_reverse]


# Get the exchange rates from the API
rates = {}
logging.info('Get the ECB exchange rates for: %s', currencies)
for currency in currencies:
    rates[currency], rates[currency]['date'] = get_api_rates(currency)
    time.sleep(1)

# rates is now a dictionary with a key-value pair for each base currency
# the value is another dictionary with key-value pairs of all the currencies and rates - followed by 'date' and an ISO date-string
# example:
# {
#      'EUR': {
#           'CAD': 0.1363670099,
#           'HKD': 0.8059745802,
#           'USD': 1.1072,
#           'date': '2019-08-29'
#     },
#     'USD': {
#           'CAD': 1.3275830925,
#           'HKD': 7.8464595376,
#           'EUR': 0.9031791908,
#           'date': '2019-08-29'
#     }
# }


# Okay, now that rates is built, let's start constructing our output.
logging.info('Data from ECB received, start constructing the output')
json_data = []

# for currency in currencies -- currencies holds a unique list, so we don't risk double-generating anything
# then build the list of companies using that currency
# extract the date for that currency
# loop through all the exchange rates for that currency
# avoid mistaking the 'date' entry for an exchange rate
# lastly, generate the currency-pair (forward and reverse rate) one-by-one and extend the json_data list with the result
for currency in currencies:
    company_list = get_companies_by_currency(currency)
    date = rates[currency]['date']
    for rate in rates[currency]:
        if rate != 'date':
            exchange_rate = rates[currency][rate]
            json_data.extend(generate_currency_pair(
                currency, rate, company_list, exchange_rate, date))


logging.info('Output constructed, add timestamps')
# add 'lastUpdated' timestamps
json_data = add_timestamps(json_data)


logging.info('Save a local JSON copy to: exchange_rates.json')
# Let's save a copy
with open('exchange_rates.json', 'w') as f:
    json.dump(json_data, f, indent=4, sort_keys=True)

# and then post it
logging.info('Post the exchange rates JSON to the API')
response = post_api_rates(json_data)
logging.info('API called, returned: %s', response.status_code)
# response.raise_for_status()

logging.info('Store full API response as api_response.txt')
# and just in case, let's save the API response
with open('api_response.txt', 'w') as f:
    f.write(response.url + " returned HTTP status code: " +
            str(response.status_code) + '\n')
    f.write(response.text)
