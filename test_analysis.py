from src.storage import execute_sql_file

def run_analysis():
    print("--- Calculating Volatility ---")
    df_volatility = execute_sql_file('sql/01_volatility.sql')
    print(df_volatility)
    
    print("\n--- Calculating Moving Averages (First 5 rows) ---")
    df_ma = execute_sql_file('sql/02_moving_avg.sql')
    print(df_ma.head())

if __name__ == "__main__":
    run_analysis()