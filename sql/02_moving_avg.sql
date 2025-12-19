SELECT 
    date,
    ticker,
    close,
    -- AVG(close) over the last 30 rows (current row + 29 previous)
    AVG(close) OVER (
        PARTITION BY ticker 
        ORDER BY date 
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as ma_30_day
FROM stock_prices
ORDER BY ticker, date DESC;