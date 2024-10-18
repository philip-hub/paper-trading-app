import yfinance as yf
import csv
from datetime import datetime
from datetime import timedelta

# Fetch real-time stock price using Yahoo Finance
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    try:
        price = stock.history(period="1d")['Close'].iloc[-1]  # Get the last close price
        return price
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Fetch historical stock price for a specific date using Yahoo Finance
def get_stock_price_on_date(ticker, date):
    stock = yf.Ticker(ticker)
    try:
        history = stock.history(start=date, end=(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d'))
        if not history.empty:
            return history['Close'].iloc[0]  # Return the close price on that date
        else:
            print(f"No data returned for {ticker} on {date}. Trying the nearest available trading day.")
            # Retry with the previous available date
            history = stock.history(period="5d")  # Fetch last 5 trading days
            if not history.empty:
                return history['Close'].iloc[-1]  # Return the most recent close price
            else:
                print(f"Failed to find any recent data for {ticker}")
                return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
    
# Check current positions and calculate open gain
def check_positions():
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
                purchase_price = get_stock_price_on_date(ticker, buy_date)
                current_price = get_stock_price(ticker)
                if purchase_price is not None and current_price is not None:
                    open_gain = (current_price - purchase_price) * amount
                    print(f"Ticker: {ticker}, Amount: {amount}, Buy Date: {buy_date}, Open Gain: ${open_gain:.2f}")
                else:
                    print(f"Failed to calculate open gain for {ticker}.")
    except FileNotFoundError:
        print("No positions file found.")

# Buy stock and update the positions
def buy_stock(ticker, amount):
    current_price = get_stock_price(ticker)
    buy_date = datetime.today().strftime('%Y-%m-%d')
    if current_price is None:
        print(f"Failed to get the current price for {ticker}")
        return
    positions = []
    stock_found = False
    try:
        with open('positions.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == ticker:
                    new_amount = int(row[1]) + amount
                    positions.append([ticker, new_amount, row[2]])  # Keep original buy_date
                    stock_found = True
                else:
                    positions.append(row)
    except FileNotFoundError:
        pass
    if not stock_found:
        positions.append([ticker, amount, buy_date])
    with open('positions.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(positions)
    with open('transactions.txt', mode='a') as file:
        file.write(f"{datetime.now()} - Bought {amount} of {ticker} at {current_price}\n")
    print(f"Bought {amount} of {ticker} at {current_price}")

# Main menu for trading
def main():
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
            buy_stock(ticker, amount)
        elif choice == "3":
            check_positions()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
