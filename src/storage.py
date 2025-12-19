import sqlite3
import pandas as pd
import os

# 1. Get the folder where THIS file (storage.py) lives: ".../src"
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to the project root: ".../stock-portfolio-analyzer"
project_root = os.path.dirname(current_dir)

# 3. Build the absolute path to the database
DB_NAME = os.path.join(project_root, "data", "portfolio.db")
# ----------------

def save_to_sqlite(df: pd.DataFrame, table_name: str = "stock_prices"):
    """
    Saves a Pandas DataFrame to the SQLite database.
    If the table exists, it replaces it (ensuring fresh data).
    """
    try:
        # Connect to the database using the ABSOLUTE path
        conn = sqlite3.connect(DB_NAME)
        
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✔ Successfully saved {len(df)} rows to table '{table_name}' in {DB_NAME}")
        
    except Exception as e:
        print(f"✘ Error saving to database: {e}")
        
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def execute_sql_query(query: str) -> pd.DataFrame:
    """
    Executes a raw SQL query string and returns the result as a DataFrame.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"✘ Database Error: {e}")
        return pd.DataFrame()
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def execute_sql_file(file_path: str) -> pd.DataFrame:
    """
    Reads a .sql file and executes it.
    """
    try:
        # If the file path passed is relative (e.g. '../sql/file.sql'), 
        # we need to make sure we find it relative to the NOTEBOOK or SCRIPT running it.
        # Ideally, pass absolute paths, but for now we try to open it directly.
        with open(file_path, 'r') as f:
            query = f.read()
            
        print(f"--- Executing SQL file: {file_path} ---")
        return execute_sql_query(query)
        
    except FileNotFoundError:
        print(f"✘ Error: The file {file_path} was not found.")
        return pd.DataFrame()