import yfinance as yf
import pandas as pd
from typing import List

def fetch_stock_data(tickers: List[str]) -> pd.DataFrame:
    """
    Fetches the last 2 years of daily closing prices and volume 
    for the provided list of tickers using yfinance.

    Args:
        tickers (List[str]): A list of stock symbols (e.g., ['AAPL', 'MSFT'])

    Returns:
        pd.DataFrame: A combined DataFrame with columns [date, ticker, close, volume]
    """
    print(f"--- Fetching data for: {', '.join(tickers)} ---")
    data_frames = []
    
    for ticker in tickers:
        try:
            # Download 2 years of data
            # progress=False hides the default yfinance loading bar to keep our logs clean
            df = yf.download(ticker, period="2y", progress=False)
            
            if df.empty:
                print(f"Warning: No data found for {ticker}")
                continue

            # yfinance returns 'Date' as the index. We want it as a column.
            df = df.reset_index()
            
            # Keep only the columns we need for our analysis
            # We use .copy() to avoid SettingWithCopy warnings
            clean_df = df[['Date', 'Close', 'Volume']].copy()
            
            # Rename columns to match our SQL schema (lowercase is standard in SQL)
            clean_df.columns = ['date', 'close', 'volume']
            
            # Add the ticker identifier
            clean_df['ticker'] = ticker
            
            # Convert timestamp to simple string format (YYYY-MM-DD)
            # This makes it much easier to read in SQLite
            clean_df['date'] = clean_df['date'].dt.strftime('%Y-%m-%d')
            
            data_frames.append(clean_df)
            print(f"✔ Successfully loaded {len(clean_df)} rows for {ticker}")
            
        except Exception as e:
            print(f"✘ Error fetching {ticker}: {e}")

    # If we found no data at all, return an empty dataframe
    if not data_frames:
        return pd.DataFrame()
        
    # Combine all individual stock dataframes into one big table
    return pd.concat(data_frames, ignore_index=True)

if __name__ == "__main__":
    # Test block: This only runs if you run this file directly
    # usage: python src/extraction.py
    test_data = fetch_stock_data(['AAPL'])
    print(test_data.head())