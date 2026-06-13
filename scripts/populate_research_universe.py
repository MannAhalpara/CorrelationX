import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://neondb_owner:npg_GN7uD0xOIXpR@ep-icy-heart-ao8tz1lj-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

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