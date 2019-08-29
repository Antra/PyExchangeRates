import requests
import json
from datetime import datetime
import time
import uuid


# Some basics
exchange_rate_url = 'https://api.exchangeratesapi.io/latest'
companies = {'NG': '',
             'NG100': 'EUR',
             'NG200': 'USD',
             'NG300': 'GBP',
             'NG400': 'NOK',
             'NG500': 'SEK',
             'NG600': 'JPY',
             'NG700': 'MXN'}
currencies = set(filter(None, companies.values()))
basware_exchange_rate_url = 'https://test-api.basware.com/v1/exchangeRates'

# add API username and password inside the single-quotes below, e.g.: auth = ('api-user', 'secret-password')
auth = ('user', 'pass')


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

    # generate the 'forward' exchange rate; currency1 (base) -> currency2
    currency_pair['rate'] = rate
    currency_pair['currencyCodeTo'] = currency1
    currency_pair['currencyCodeFrom'] = currency2
    currency_pair['validFrom'] = date
    currency_pair['companies'] = company_list
    currency_pair['externalCode'] = str(uuid.uuid4())
    currency_pair['lastUpdated'] = ''
    # generate the 'reverse' exchange rate; currency2 -> currency1 (base)
    currency_pair_reverse['rate'] = get_reverse_rate(rate)
    currency_pair_reverse['currencyCodeTo'] = currency2
    currency_pair_reverse['currencyCodeFrom'] = currency1
    currency_pair_reverse['validFrom'] = date
    currency_pair_reverse['companies'] = company_list
    currency_pair_reverse['externalCode'] = str(uuid.uuid4())
    currency_pair_reverse['lastUpdated'] = ''
    # return the currency pairs as a list to make life easier
    return [currency_pair, currency_pair_reverse]


rates = {}
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
#           'USD': 1.1072
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
json_data = []

# for currency in currencies -- currencies holds a unique list, so we don't risk double-generating anything
# - company_list = get_companies_by_currency(currency)
# - date = rates[currency][date]
# - for rate in rates[currency]:
# -- if rate != 'date':
# --- exchange_rate = rates[currency][rate]
# --- json_data.extend(generate_currency_pair(currency, rate, company_list, exchange_rate, date))

for currency in currencies:
    company_list = get_companies_by_currency(currency)
    date = rates[currency]['date']
    for rate in rates[currency]:
        if rate != 'date':
            exchange_rate = rates[currency][rate]
            json_data.extend(generate_currency_pair(
                currency, rate, company_list, exchange_rate, date))


# add 'lastUpdated' timestamps
json_data = add_timestamps(json_data)

# Let's save a copy
with open('exchange_rates.json', 'w') as f:
    json.dump(json_data, f)

# and then post it
response = post_api_rates(json_data)
response.raise_for_status()

# and just in case, let's save the API response
with open('api_response.txt', 'w') as f:
    f.write(response.url + " returned HTTP status code: " +
            str(response.status_code) + '\n')
    f.write(response.text)
