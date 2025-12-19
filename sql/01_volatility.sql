WITH DailyReturns AS (
    SELECT 
        ticker,
        date,
        close,
        -- Window Function: Look at the previous row's close
        LAG(close) OVER (PARTITION BY ticker ORDER BY date) as prev_close,
        -- Calculate Daily Return: (Today - Yesterday) / Yesterday
        (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
        / LAG(close) OVER (PARTITION BY ticker ORDER BY date) as dr
    FROM stock_prices
),
Stats AS (
    SELECT 
        ticker,
        -- Calculate the Average Daily Return (Mean)
        AVG(dr) as mean_return,
        -- Count how many days of data we have
        COUNT(dr) as n
    FROM DailyReturns
    WHERE dr IS NOT NULL -- The first day is always NULL because there is no "yesterday"
    GROUP BY ticker
)
SELECT 
    dr.ticker,
    -- VARIANCE Formula: Sum of (Value - Mean)^2 / (N - 1)
    SUM((dr.dr - s.mean_return) * (dr.dr - s.mean_return)) / (s.n - 1) as variance,
    -- VOLATILITY (Approximation): Square Root of Variance (Calculated in Python later)
    -- Note: SQLite lacks a SQRT function, so we export Variance.
    COUNT(dr.dr) as days_observed
FROM DailyReturns dr
JOIN Stats s ON dr.ticker = s.ticker
WHERE dr.dr IS NOT NULL
GROUP BY dr.ticker
ORDER BY variance DESC;