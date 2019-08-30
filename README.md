# PyExchangeRates
Basic Python script that queries European Central Bank (ECB): `https://api.exchangeratesapi.io/latest`, reshapes it to Basware-JSON and posts it to BaswareAPI.

# Usage
## Requirements
Python 3.7 and the `requests` package.

## Configuration
1. Add the basic unit structure together with their base-currency in `companies`.
1. Add the BaswareAPI credentials in `auth` - NB, username and password should still be surrounded by `'`.
1. If the BaswareAPI to use is not Test, then update `basware_exchange_rate_url` with the correct URI

## Execution
Run `main.py`, e.g. `python main.py`

## Output
The fetched exchange rates themselves are saved as `exchange_rates.json`, the latest BaswareAPI response is saved as `api_response.txt`.