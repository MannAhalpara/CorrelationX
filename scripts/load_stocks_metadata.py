import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://neondb_owner:npg_GN7uD0xOIXpR@ep-icy-heart-ao8tz1lj-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

sectors = {
    "IT": ["INFY.NS", "TCS.NS", "WIPRO.NS", "TECHM.NS", "HCLTECH.NS", "LTTS.NS", "MPHASIS.NS", "COFORGE.NS", "PERSISTENT.NS", "SONACOMS.NS"],
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS", "IDFCFIRSTB.NS", "PNB.NS", "BANKBARODA.NS", "FEDERALBNK.NS", "INDUSINDBK.NS"],
    "Pharma": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "AUROPHARMA.NS", "BIOCON.NS", "LUPIN.NS", "DIVISLAB.NS", "GLENMARK.NS", "ZYDUSLIFE.NS", "ALKEM.NS"],
    "Auto": ["TATAMOTORS.NS", "MARUTI.NS", "M&M.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "ASHOKLEY.NS", "HEROMOTOCO.NS", "TVSMOTOR.NS", "BALKRISIND.NS", "AMARAJABAT.NS"],
    "FMCG": ["ITC.NS", "HINDUNILVR.NS", "BRITANNIA.NS", "NESTLEIND.NS", "DABUR.NS", "MARICO.NS", "TATACONSUM.NS", "GODREJCP.NS", "EMAMILTD.NS", "COLPAL.NS"],
    "Energy": ["RELIANCE.NS", "ONGC.NS", "GAIL.NS", "IOC.NS", "BPCL.NS", "NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "ADANIGREEN.NS", "ADANITRANS.NS"],
    "Metals": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "NATIONALUM.NS", "JINDALSTEL.NS", "SAIL.NS", "HINDZINC.NS", "MOIL.NS"],
    "RealEstate": ["DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PHOENIXLTD.NS", "SOBHA.NS", "PRESTIGE.NS", "BRIGADE.NS", "SUNTECK.NS", "LODHA.NS", "IBREALEST.NS"],
    "Telecom": ["BHARTIARTL.NS", "IDEA.NS", "TATACOMM.NS", "MTNL.NS", "ROUTEMOBILE.NS", "TEJASNET.NS", "HFCL.NS", "INDUSTOWER.NS", "STLTECH.NS", "ONMOBILE.NS"],
    "ConsumerDurables": ["VGUARD.NS", "WHIRLPOOL.NS", "CROMPTON.NS", "HAVELLS.NS", "BAJAJELEC.NS", "POLYCAB.NS", "VOLTAS.NS", "DIXON.NS", "ORIENTELEC.NS", "BOSCHLTD.NS"]
}

rows = []

for sector, tickers in sectors.items():
    for ticker in tickers:
        rows.append({
    "ticker": ticker,
    "company_name": ticker.replace(".NS", ""),
    "sector": sector
})

df = pd.DataFrame(rows)

df.to_sql(
    "stocks",
    engine,
    if_exists="append",
    index=False
)

print(f"Inserted {len(df)} stocks")