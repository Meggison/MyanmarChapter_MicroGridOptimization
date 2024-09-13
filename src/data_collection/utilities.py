from joblib import Memory
import pandas as pd

# setup job lib cache
mem_cache = Memory('cache')


def comparable_date(date: str):
    return (pd.to_datetime(date) - pd.DateOffset(days=364)).strftime("%Y-%m-%d")
