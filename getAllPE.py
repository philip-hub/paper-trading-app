import yfinance as yf
import csv

# Step 1: Read tickers from the file
def read_tickers_from_file(file_path):
    with open(file_path, 'r') as file:
        tickers = [line.strip() for line in file.readlines()]
    return tickers

# Step 2: Get PE ratio for a ticker from Yahoo Finance
def get_pe_ratio(ticker):
    try:
        stock = yf.Ticker(ticker)
        pe_ratio = stock.info.get('trailingPE')
        if pe_ratio is None or isinstance(pe_ratio, str):
            return None
        return float(pe_ratio)
    except Exception as e:
        print(f"Error fetching PE ratio for {ticker}: {e}")
        return None

# Step 3: Loop through tickers and fetch PE ratios for profitable companies
def fetch_pe_ratios(tickers):
    pe_ratios = []
    for ticker in tickers:
        print(ticker)
        pe_ratio = get_pe_ratio(ticker)
        if pe_ratio is not None and pe_ratio > 0:  # Only consider profitable companies
            pe_ratios.append((ticker, pe_ratio))
    return pe_ratios

# Step 4: Save results to a CSV, sorted by PE ratio
def save_to_csv(pe_ratios, file_name):
    # Sort by PE ratio (2nd column in tuple)
    pe_ratios_sorted = sorted(pe_ratios, key=lambda x: x[1])
    
    # Write to CSV
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Ticker', 'PE Ratio'])
        writer.writerows(pe_ratios_sorted)
    print(f"Saved to {file_name}")

# Main function to run the script
def main():
    tickers = read_tickers_from_file('nyse_tickers.txt')  # Adjust the file path as needed
    pe_ratios = fetch_pe_ratios(tickers)
    save_to_csv(pe_ratios, 'sorted_pe_ratios.csv')

if __name__ == "__main__":
    main()

