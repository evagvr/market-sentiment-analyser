import pandas as pd
import yfinance as yf
from datetime import datetime


class StockScraper:
    def __init__(self, ticker: str):
        self.ticker = ticker
        # Hint: You might want to initialize the yf.Ticker object here

    def fetch_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch historical stock prices for the given date range.

        Inputs: start_date and end_date as strings (e.g., '2026-03-18')
        Output: A cleaned pandas DataFrame containing Date, Open, High, Low, Close, Volume.
        """
        # Step 1: Use the yfinance library to get historical data for the date range.
        # Step 2: yfinance returns a DataFrame where the 'Date' is the index.
        #         Reset the index so 'Date' becomes a normal column.
        # Step 3: Ensure the 'Date' column is formatted exactly the same way
        #         as the 'date' column in your NewsScraper (just the date, no time).
        # Step 4: Return the cleaned DataFrame.
        pass

    def save_raw(self, df: pd.DataFrame):
        """
        Save the DataFrame to a CSV file in the data/raw/ directory.
        Keep the naming convention similar to your news scraper.
        """
        pass

# Add an 'if __name__ == "__main__":' block at the bottom to test it
# exactly like you did in scraper.py