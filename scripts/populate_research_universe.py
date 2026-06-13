import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

query = """
SELECT ticker
FROM prices
GROUP BY ticker
HAVING MIN(date) <= DATE '2015-01-01'
ORDER BY ticker
"""

df = pd.read_sql(query, engine)

print(f"Found {len(df)} eligible stocks")

df.to_sql(
    "research_universe",
    engine,
    if_exists="append",
    index=False
)

print("Research universe populated successfully!")