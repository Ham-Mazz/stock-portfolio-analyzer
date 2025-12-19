# Quantitative Stock Portfolio Analyzer: SQL-First Financial Analytics

## Project Overview
This project explores the implementation of institutional-grade financial metrics using SQL rather than traditional in-memory Python libraries.

We aim to demonstrate a SQL-First Architecture, where heavy statistical lifting—such as rolling averages and variance calculations—is offloaded to the database engine (SQLite) to simulate a scalable, production-ready data warehouse environment.

## The Architectural Approaches

### Traditional In-Memory (The Context):
* Relies on libraries like Pandas to compute metrics in the application layer (RAM).
* **Limitation:** While easy to write, this approach becomes a bottleneck with terabyte-scale financial datasets, as all raw data must be moved to the client.

### In-Database SQL (This Project):
* Pushes computation directly to the storage layer (SQLite).
* Utilizes Window Functions (`OVER`, `PARTITION BY`) and CTEs to perform complex time-series analysis.
* **Advantage:** Logic is executed where the data lives, reducing network overhead and enabling analysis on datasets larger than available RAM.

### The Goal
To validate that complex "black box" indicators—specifically Volatility and Moving Averages—can be mathematically reconstructed using raw, transparent SQL logic, ensuring reproducibility and scalability.


## Installation

### Clone the repository:
```bash
git clone [https://github.com/YOUR-USERNAME/stock-portfolio-analyzer.git](https://github.com/YOUR-USERNAME/stock-portfolio-analyzer.git)
cd stock-portfolio-analyzer
```

### Install Dependencies:
This project relies on `yfinance` for the API gateway and `pandas` for data transport.

```bash
pip install -r requirements.txt
```

## Usage

### 1. Run the ETL Pipeline
To reproduce the dataset, run the main orchestrator. This script fetches raw OHLCV data from the Yahoo Finance API, normalizes it, and loads it into the data warehouse (`data/portfolio.db`).

```bash
python main.py
```

> **Note:** This script is idempotent. You can run it multiple times without creating duplicate records (`if_exists='replace'` strategy).

### 2. Visualize the Results
Launch the executive dashboard to view the SQL-derived metrics and render the charts.

```bash
jupyter notebook notebooks/analysis.ipynb
```

Inside the notebook, the `execute_sql_file` wrapper handles the connection between the Python presentation layer and the SQL logic layer.

## Project Structure

* **src/extraction.py:** The API Gateway. Handles connection to external data sources (`yfinance`), manages rate limiting, and cleans raw data frames.
* **src/storage.py:** The Persistence Manager. Manages SQLite connections and context, ensuring safe write operations and preventing database locks.
* **sql/01_volatility.sql:** The Risk Engine. Uses complex CTEs and manual Variance calculations ($\sum(x-\overline{x})^{2}$) to derive standard deviation without built-in functions.
* **sql/02_moving_avg.sql:** The Trend Engine. Implements Window Functions (`ROWS BETWEEN...`) to calculate rolling averages.
* **main.py:** The Orchestrator. Ties the extraction and storage modules together into a unified pipeline.
* **notebooks/analysis.ipynb:** The Interface. A Jupyter notebook that acts as the frontend for the project.