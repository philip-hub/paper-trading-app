import requests
from polygon.rest import RESTClient

def get_api_key():
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.read().strip()  # Strip any extra whitespace
            return api_key
    except FileNotFoundError:
        print("Error: 'api_key.txt' file not found. Please create the file and add your Polygon.io API key.")
        return None

def get_stock_price(ticker, api_key,date):
    # Initialize the client
    client = RESTClient(api_key)
    
    # Retrieve the most recent aggregate data (for example: 1-day candles)
    try:
        aggs = list(client.list_aggs(
            ticker, 
            1, 
            "day", 
            "2024-10-07",  # Adjust the date range as needed
            date,  # Adjust this to the current date or dynamically
            limit=1  # Limit to 1 to get the most recent result
        ))
        
        if len(aggs) > 0:
            return aggs[0].close  # Return the close price of the most recent aggregate
        
        print(f"No data returned for {ticker}")
        return None

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Call the API key function to get the actual API key
api_key = get_api_key()
date = "2024-10-08"
# Now pass the API key string to get_stock_price
if api_key:
    print(get_stock_price("NVDA", api_key,date))


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
           
