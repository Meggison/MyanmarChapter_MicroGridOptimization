""" Appliance definitions for rural Myanmar.

Schedule, notes, and occurrences are taken from the case study in https://www.mdpi.com/1996-1073/13/20/5313
village: Thae Kone, Myanmar (has relatively easy access to Mandalay city)
households: 300
average household size: 5.1 persons
average household income: 39,178 MMK/household/month or about 28.7 USD/household/month (March 2020 conversion rate)
sample: 100 survey participants with 85% eligible answers.


Myanmar typical daily schedule:
-----------------------------------------------------------------------------
| Activities             | Main Time                     | Duration (Hours) |
|------------------------|-------------------------------|------------------|
| Washing/Bathing        | 6:00-8:00, 18:00-18:45        | 0.5-1            |
| Commuting (1 way)      | 6:00-9:00, 16:00-19:00        | 0.5-1.5          |
| Work                   | 8:00-18:00                    | 7-10             |
| Studying/Homework      | 8:00-16:00, 18:00-20:00       | 6-9              |
| Family care/housework  | 6:00-7:00, 18:00-20:00        | 1-5              |
| Cooking                | 5:00-7:00                     | 0.5-2            |
| Resting/Entertainment  | 18:00-22:00                   | 0.5-5            |
| Shopping/others        | 6:00-9:00                     | 0.5-1            |
| Eating                 | 5:30-8:30, 12:00-13:00, 17:30-19:30 | 1-1.5     |

Appliance notes:
-----------------------------------------------------------------------------
| Item                                         | Myanmar                                                                                                                                                     |
|----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Average floor area (m²)                      | 50                                                                                                                                                           |
| Lighting appliance                           | 74.6 W Fluorescent lamp                                                                                                                                      |
| Lighting appliances simultaneous operating rate | 0.7                                                                                                                                                        |
| Air Conditioner operation period *           | 9.6 weeks from 22nd March to 28th May Weekday 2 h/d (18:00-20:00), Weekend 8 h/d (12:00-20:00)                                                                |
| Air conditioner (W)                          | 800                                                                                                                                                          |
| Electric fan operation period *              | 8 months from March to November, Average of 5 h/d                                                                                                            |
| Electric fan (W)                             | 100                                                                                                                                                          |
| Television (W)                               | 70                                                                                                                                                           |
| Refrigerator (W)                             | 200                                                                                                                                                          |
| Water pump (W)                               | 320                                                                                                                                                          |
| Radio (W)                                    | 2.4                                                                                                                                                          |
| Rice cooker                                  | Not used ?????????                                                                                                                                         |                                                                                                                                                 |
| Washing machine                              | 400                                                                                                                                                          |
| Cellphone charging                           | Charging time: 2.25 h/d Charging wattage: 5                                                                                                                   |

"""

import numpy as np
import pandas as pd
from ramp import User, UseCase
import random
from tqdm import tqdm
from src.data_collection.utilities import comparable_date
from src.model_development.optimization.demand.definitions import appliance_usage
from src.data_collection.renewable_ninja import get_heating_demand
from src.data_collection.utilities import mem_cache

appliance_aliases = {
    "air conditioner": ["air conditioner (weekday)", "air conditioner (weekend)"],
}


# seasonality is based MMSIS & renewable ninja cooling demand
appliance_seasonality = {
    "air conditioner": True,
    "electric fan": True,
}

appliance_occurrences = {
    "air conditioner": 0.494,
    "cellphone charging": 0.951,
    "electric fan": 0.741,
    "lighting": 0.951,
    "radio": 0.346,
    "refrigerator": 0.160,
    # "rice cooker": 0.222,
    "television": 0.864,
    "washing machine": 0.037,
    "water pump": 0.790,
}

@mem_cache.cache
def build_settlement_demand(
    num_households: int, date_start: str, num_days: int, lat: int, lon: int
):
    appliances = [
        [
            appliance
            for appliance, occurrence in appliance_occurrences.items()
            if random.random() < occurrence
        ]
        for _ in range(num_households)
    ]
    daily = []
    dates = [
        str(date.date())
        for date in list(pd.date_range(start=date_start, periods=num_days, freq="D"))
    ]
    # comparable dates for last year's cooling demand: "the poor man's forecast"
    start_comparable_date = comparable_date(date_start)
    end_comparable_date = comparable_date(dates[-1])
    cooling = get_heating_demand(start_comparable_date, end_comparable_date, lat, lon)
    for date in tqdm(dates, desc="Processing", unit="dates"):
        households = [
            User(
                user_name=f"household #{i}",
                num_users=1,
            )
            for i in range(num_households)
        ]
        comparable = comparable_date(date)
        cooling_demand = cooling[comparable]["cooling_demand"]
        for i, household in enumerate(households):
            for appliance in appliances[i]:
                seasonal = appliance_seasonality.get(appliance, False)
                aliases = appliance_aliases.get(appliance, [appliance])
                for alias in aliases:
                    definition = appliance_usage[alias]
                    if seasonal:
                        definition = dict(definition)
                        definition["power"] *= min(cooling_demand, 1)
                    household.add_appliance(name=appliance, **definition)
        settlement = UseCase(users=households, date_start=date)
        settlement.initialize(num_days=1)
        demand = settlement.generate_daily_load_profiles()
        daily.append(demand)
    demand = np.concatenate(daily)
    timestamps = pd.date_range(start=date_start, periods=1440 * num_days, freq="min")
    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "date": timestamps.strftime("%Y-%m-%d"),
            "time": timestamps.strftime("%H:%M"),
            "kW": demand / 1000,
        }
    )
    df["date"] = pd.to_datetime(df["date"])
    return df
