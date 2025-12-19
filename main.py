from src.extraction import fetch_stock_data
from src.storage import save_to_sqlite

def main():
    print("--- Starting Stock Portfolio ETL ---")
    
    # 1. Configuration
    tickers = ['AAPL', 'MSFT', 'TSLA']
    
    # 2. Extract
    df = fetch_stock_data(tickers)
    
    # 3. Load
    if not df.empty:
        save_to_sqlite(df)
        print("--- ETL Process Completed Successfully ---")
    else:
        print("--- ETL Failed: No data fetched ---")

if __name__ == "__main__":
    main()