import requests

def get_stock_price(ticker, api_key):
    url = f"https://api.polygon.io/v1/last/stocks/{ticker}?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['last']['price']


def get_api_key():
    # Read the API key from the file
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        print("Error: 'api_key.txt' file not found. Please create the file and add your Polygon.io API key.")
        return None


get_stock_price("NVDA", get_api_key)

# def main():
#     api_key = get_api_key()
#     if api_key is None:
#         return  # Exit if the API key could not be read
    
#     while True:
#         print("1. Buy Stock")
#         print("2. Sell Stock")
#         print("3. Display Gains")
#         print("4. Exit")
        
#         choice = input("Choose an option: ")
#         if choice == "1":
#             ticker = input("Enter stock ticker: ")
#             amount = int(input("Enter amount: "))
#             buy_stock(ticker, amount, api_key)
#         elif choice == "2":
#             ticker = input("Enter stock ticker: ")
#             amount = int(input("Enter amount: "))
           
