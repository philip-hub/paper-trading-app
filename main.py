

import requests

def get_stock_price(ticker, api_key):
    url = f"https://api.polygon.io/v1/last/stocks/{ticker}?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['last']['price']
