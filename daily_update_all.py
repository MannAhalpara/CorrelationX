import pandas as pd
import yfinance as yf

from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
    
engine = create_engine("postgresql://neondb_owner:npg_GN7uD0xOIXpR@ep-icy-heart-ao8tz1lj-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

# Get only research universe stocks
query = """
SELECT ticker
FROM research_universe
ORDER BY ticker
"""

tickers = pd.read_sql(query, engine)["ticker"].tolist()

print(f"Found {len(tickers)} stocks")


for ticker in tickers:

    try:

        print(f"\nProcessing {ticker}")

        last_date_query = f"""
        SELECT MAX(date) AS last_date
        FROM prices
        WHERE ticker = '{ticker}'
        """

        last_date = pd.read_sql(
            last_date_query,
            engine
        ).iloc[0]["last_date"]

        start_date = last_date + timedelta(days=1)

        data = yf.download(
            ticker,
            start=start_date.strftime("%Y-%m-%d"),
            end=(datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
            auto_adjust=True,
            progress=False
        )

        if data.empty:
            print("No new data")
            continue

        data.columns = data.columns.get_level_values(0)

        data.reset_index(inplace=True)

        data.rename(columns={
            "Date": "date",
            "Open": "open_price",
            "High": "high_price",
            "Low": "low_price",
            "Close": "close_price",
            "Volume": "volume"
        }, inplace=True)

        data["ticker"] = ticker

        data = data[
            [
                "ticker",
                "date",
                "open_price",
                "high_price",
                "low_price",
                "close_price",
                "volume"
            ]
        ]

        # safer than to_sql later
        data.to_sql(
            "prices",
            engine,
            if_exists="append",
            index=False
        )

        print(f"Inserted {len(data)} rows")

    except Exception as e:
        print(f"Failed {ticker}: {e}")