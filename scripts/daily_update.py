from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

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