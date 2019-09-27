# PyExchangeRates
Basic Python script that queries European Central Bank (ECB): `https://api.exchangeratesapi.io/latest`,  
reshapes it to Basware-JSON and posts it to BaswareAPI.

# Disclaimer
This software is made as an own "hobby project" and is not an official Basware product.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
SOFTWARE.

# Usage
## Requirements
Python 3.7 and the `requests` package, e.g.:
```python -m pip install requests```

## Configuration
1. Add the basic unit structure together with their base-currency in the `companies` dictionary.
1. Add the BaswareAPI credentials in the `auth` tuple - NB, username and password should still be surrounded by `'`.
1. If the BaswareAPI to use is not Test, then update `basware_exchange_rate_url` with the correct URI

## Execution
Run `main.py`, e.g. `python main.py`

## Output
The script will not output anything to the console, but the result will be that the most recent ECB exchange rates will be posted to Basware API.  
They should appear within Basware P2P within a short timeframe (<5 mins).

## Logging
- the script will keep the most recent execution in as `logs/rates.log`
- the most recent BaswareAPI response is saved as `api_response.txt`
- the most recent fetched exchange rates are saved as `exchange_rates.json`

# Comments/Feedback/Contributions
Comments and feedback is welcome, just reach out to me.

You're welcome to contribute to this repo by submitting pull requests and creating issues.  
For pull requests, please split complex changes into multiple pull requests when feasible, use one commit per pull request, and try to follow the existing code style.

Anders Demant van der Weide