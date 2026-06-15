import os

import pandas as pd

from itertools import combinations

from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import kendalltau

from sqlalchemy import create_engine
from sqlalchemy import text

from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


print("Loading research universe...")

tickers = pd.read_sql(
    """
    SELECT ticker
    FROM research_universe
    ORDER BY ticker
    """,
    engine
)["ticker"].tolist()

print(f"{len(tickers)} stocks found")


print("Loading prices...")

prices = pd.read_sql(
    """
    SELECT
        ticker,
        date,
        close_price
    FROM prices
    WHERE ticker IN (
        SELECT ticker
        FROM research_universe
    )
    """,
    engine
)

prices["date"] = pd.to_datetime(prices["date"])

print(f"{len(prices)} price rows loaded")


print("Clearing old correlations...")

with engine.begin() as conn:

    conn.execute(
        text("TRUNCATE TABLE pearson_correlations")
    )

    conn.execute(
        text("TRUNCATE TABLE spearman_correlations")
    )

    conn.execute(
        text("TRUNCATE TABLE kendall_correlations")
    )

print("Old correlations removed")


pearson_rows = []
spearman_rows = []
kendall_rows = []


total_pairs = len(tickers) * (len(tickers) - 1) // 2

print(f"Total pairs: {total_pairs}")

pair_count = 0


for ticker_1, ticker_2 in combinations(tickers, 2):

    pair_count += 1

    if pair_count % 100 == 0:
        print(
            f"Processed {pair_count}/{total_pairs} pairs"
        )

    stock_1 = prices[
        prices["ticker"] == ticker_1
    ][["date", "close_price"]]

    stock_2 = prices[
        prices["ticker"] == ticker_2
    ][["date", "close_price"]]

    merged = stock_1.merge(
        stock_2,
        on="date",
        suffixes=("_1", "_2")
    )

    if len(merged) < 30:
        continue

    x = merged["close_price_1"]
    y = merged["close_price_2"]

    try:

        pearson_value, _ = pearsonr(x, y)
        spearman_value, _ = spearmanr(x, y)
        kendall_value, _ = kendalltau(x, y)

        start_date = merged["date"].min().date()
        end_date = merged["date"].max().date()

        pearson_rows.append(
            {
                "ticker_1": ticker_1,
                "ticker_2": ticker_2,
                "correlation": float(pearson_value),
                "start_date": start_date,
                "end_date": end_date
            }
        )

        spearman_rows.append(
            {
                "ticker_1": ticker_1,
                "ticker_2": ticker_2,
                "correlation": float(spearman_value),
                "start_date": start_date,
                "end_date": end_date
            }
        )

        kendall_rows.append(
            {
                "ticker_1": ticker_1,
                "ticker_2": ticker_2,
                "correlation": float(kendall_value),
                "start_date": start_date,
                "end_date": end_date
            }
        )

    except Exception as e:

        print(
            f"Failed: {ticker_1} - {ticker_2}"
        )

        print(e)


print("\nSaving Pearson correlations...")

pd.DataFrame(
    pearson_rows
).to_sql(
    "pearson_correlations",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)


print("Saving Spearman correlations...")

pd.DataFrame(
    spearman_rows
).to_sql(
    "spearman_correlations",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)


print("Saving Kendall correlations...")

pd.DataFrame(
    kendall_rows
).to_sql(
    "kendall_correlations",
    engine,
    if_exists="append",
    index=False,
    chunksize=1000
)


print()
print("===================================")
print("Correlation Calculation Complete")
print("===================================")

print(f"Pearson rows : {len(pearson_rows)}")
print(f"Spearman rows: {len(spearman_rows)}")
print(f"Kendall rows : {len(kendall_rows)}")