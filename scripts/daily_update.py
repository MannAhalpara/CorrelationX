from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/correlationx"
)

query = """
SELECT
    ticker,
    MAX(date) AS last_date
FROM prices
GROUP BY ticker
ORDER BY ticker
"""

df = pd.read_sql(query, engine)

print(df.head())
print(f"\nStocks found: {len(df)}")