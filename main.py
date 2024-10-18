import requests
from polygon.rest import RESTClient
import csv
from datetime import datetime

# Load API key from file
def get_api_key():
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.read().strip()  # Strip any extra whitespace
            return api_key
    except FileNotFoundError:
        print("Error: 'api_key.txt' file not found. Please create the file and add your Polygon.io API key.")
        return None

# Fetch the latest stock price
def get_stock_price(ticker, api_key, date):
    # Initialize the client
    client = RESTClient(api_key)
    
    try:
        # Fetch the most recent 1-day aggregate
        aggs = list(client.list_aggs(
            ticker, 
            1, 
            "day", 
            "2024-10-07",  # Adjust the start date as needed
            date,  # Use the current date or a user-provided one
            limit=1
        ))
        
        if len(aggs) > 0:
            return aggs[0].close  # Return the most recent close price
        
        print(f"No data returned for {ticker}")
        return None

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def get_stock_price_on_date(ticker, api_key, date):
    # Initialize the client
    client = RESTClient(api_key)
    
    try:
        # Fetch the aggregate data for the given date
        aggs = list(client.list_aggs(
            ticker, 
            1, 
            "day", 
            date,  # Date of the stock price to fetch
            date,  # Use the same date for both from and to
            limit=1
        ))
        
        if len(aggs) > 0:
            return aggs[0].close  # Return the close price on that date
        
        print(f"No data returned for {ticker} on {date}")
        return None

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def check_positions(api_key):
    try:
        with open('positions.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row if it exists
            
            print("Current Positions and Open Gain:")
            
            for row in reader:
                ticker = row[0]
                amount = int(row[1])
                buy_date = row[2]
                
                if amount == 0:
                    continue  # Skip stocks with zero holdings
                
                # Fetch the purchase price on the buy date
                purchase_price = get_stock_price_on_date(ticker, api_key, buy_date)
                
                # Fetch the current price
                current_price = get_stock_price(ticker, api_key, datetime.today().strftime('%Y-%m-%d'))
                
                if purchase_price is not None and current_price is not None:
                    open_gain = (current_price - purchase_price) * amount
                    print(f"Ticker: {ticker}, Amount: {amount}, Buy Date: {buy_date}, Open Gain: ${open_gain:.2f}")
                else:
                    print(f"Failed to calculate open gain for {ticker}.")
    
    except FileNotFoundError:
        print("No positions file found.")


# Buy stock and update the positions, including the buy date
def buy_stock(ticker, amount, api_key):
    current_price = get_stock_price(ticker, api_key, datetime.today().strftime('%Y-%m-%d'))
    buy_date = datetime.today().strftime('%Y-%m-%d')  # Get today's date
    
    if current_price is None:
        print(f"Failed to get the current price for {ticker}")
        return
    
    # Update positions
    positions = []
    stock_found = False
    
    # Read current positions from CSV
    try:
        with open('positions.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == ticker:
                    # Update the amount if the stock already exists
                    new_amount = int(row[1]) + amount
                    positions.append([ticker, new_amount, row[2]])  # Keep the original buy_date
                    stock_found = True
                else:
                    positions.append(row)
    except FileNotFoundError:
        pass  # No positions file yet, will create it
    
    if not stock_found:
        # Add new stock if not already owned
        positions.append([ticker, amount, buy_date])
    
    # Write updated positions back to CSV
    with open('positions.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(positions)
    
    # Log the transaction
    with open('transactions.txt', mode='a') as file:
        file.write(f"{datetime.now()} - Bought {amount} of {ticker} at {current_price}\n")
    
    print(f"Bought {amount} of {ticker} at {current_price}")

# Sell stock and update the positions
def sell_stock(ticker, amount, api_key):
    current_price = get_stock_price(ticker, api_key, datetime.today().strftime('%Y-%m-%d'))
    
    if current_price is None:
        print(f"Failed to get the current price for {ticker}")
        return
    
    positions = []
    stock_found = False
    
    # Read current positions from CSV
    try:
        with open('positions.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == ticker:
                    if int(row[1]) < amount:
                        print(f"Not enough shares to sell. You own {row[1]} shares.")
                        return
                    new_amount = int(row[1]) - amount
                    if new_amount > 0:
                        positions.append([ticker, new_amount, row[2]])  # Keep the original buy_date
                    stock_found = True
                else:
                    positions.append(row)
    except FileNotFoundError:
        print(f"No positions found for {ticker}")
        return
    
    if not stock_found:
        print(f"You don't own any shares of {ticker}.")
        return
    
    # Write updated positions back to CSV
    with open('positions.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(positions)
    
    # Log the transaction
    with open('transactions.txt', mode='a') as file:
        file.write(f"{datetime.now()} - Sold {amount} of {ticker} at {current_price}\n")
    
    print(f"Sold {amount} of {ticker} at {current_price}")

# Main menu for trading
def main():
    api_key = get_api_key()
    if api_key is None:
        return  # Exit if the API key could not be read
    
    while True:
        print("\nMenu:")
        print("1. Buy Stock")
        print("2. Sell Stock")
        print("3. Check Positions")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        if choice == "1":
            ticker = input("Enter stock ticker: ").upper()
            amount = int(input("Enter amount: "))
            buy_stock(ticker, amount, api_key)
        elif choice == "2":
            ticker = input("Enter stock ticker: ").upper()
            amount = int(input("Enter amount: "))
            sell_stock(ticker, amount, api_key)
        elif choice == "3":
            check_positions(api_key)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
