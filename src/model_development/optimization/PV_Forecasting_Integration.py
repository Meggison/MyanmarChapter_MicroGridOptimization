from math import ceil
import pandas as pd
from dotenv import load_dotenv
import numpy as np
load_dotenv()

from src.data_collection.renewable_ninja import get_pv_output
from src.data_collection.supabase import get_village_cluster_data
from src.data_collection.utilities import comparable_date
from src.model_development.optimization.capacity.index import optimize_capacity
from src.model_development.optimization.demand.index import build_settlement_demand
from joblib import load
import xgboost as xgb


def run(
    cluster_id: int,
    num_days: int,
    start_date: str = pd.Timestamp.now().strftime("%Y-%m-%d"),
):
    """
    Runs the Myanmar Micro-Grid Optimization model. This includes capacity optimization, demand forecasting, and PV forecasting for a given time period.

    You need to have the following environment variables set:
    - SUPABASE_KEY: Your Supabase API key
    - RENEWABLES_NINJA_API_TOKEN: Your Renewables Ninja API token


    Parameters:
        cluster_id (int): The ID of the village cluster.
        num_days (int): The number of days to run the optimization for.
        start_date (str): The start date of the optimization period (default: current date).

    Returns:
        tuple: A tuple containing the optimal PV capacity, optimal battery capacity, optimal diesel capacity, and optimal dispatch.
    """
    cluster = get_village_cluster_data(cluster_id)
    households = ceil((cluster["Pop"] / cluster["NumPeoplePerHH"]))
    lon = cluster["X_deg"]
    lat = cluster["Y_deg"]
    demand = build_settlement_demand(
        num_households=households,
        date_start=start_date,
        num_days=num_days,
        lat=lat,
        lon=lon,
    )
    # calculate end date from start date
    # get the first day of the year prior to start date
    pv_start_date = comparable_date(demand["date"].min())
    pv_end_date = comparable_date(demand["date"].max())
    # use last years pv output for our forecast
    unit_pv = get_pv_output(pv_start_date, pv_end_date, lat, lon)
    unit_pv = pd.DataFrame(unit_pv.values())

    #added the PV model
    model = xgb.XGBRegressor(objective='reg:squarederror',
                                 n_estimators=200,
                                 subsample=1,
                                 learning_rate=0.05,
                                 max_depth=2,
                                 colsample_bytree=1,
                                 min_child_weight=5)

    model.load_model("xgboost_model.json")
    print('Model load successfull')
    #calculate features
    unit_pv['is_day_sample'] = 0   # add the value if is day or not
    unit_pv['electricity_lag_2'] = unit_pv['electricity'].shift(2)
    unit_pv['electricity_lag_2'].iloc[0:2] =0  #filling up the NaNs
    pv_vals = unit_pv["electricity"].values
    day_inp_array = unit_pv["is_day_sample"].values
    is_day_lag_2_array = unit_pv["electricity_lag_2"].values

    feature_inp_concat = np.column_stack((pv_vals, day_inp_array, is_day_lag_2_array))
    pv_forecast = model.predict(feature_inp_concat)
    print('pv_forecast')
    print(pv_forecast)

    # get optimal capacities + dispatch
    # TODO: currently this trains on the comparable time period from last year
    # for real optimal capacities, we need to train on at least a full year
    # BUT from a presentation perspective, we will get lots of curtailment if we train on the full year
    # and so I cheat :)
    # in future, we can cap it at two weeks (the most expensive weeks) to shorten the train time
    (
        optimal_pv_capacity,
        optimal_battery_capacity,
        optimal_diesel_capacity,
        optimal_dispatch,
    ) = optimize_capacity(demand.loc[::60, "kW"].values, pv_forecast)
    optimal_dispatch["timestamp"] = demand.loc[::60, "timestamp"].values
    optimal_dispatch_json = optimal_dispatch.to_json(orient="records")
    print('optimal_dispatch_json',optimal_dispatch_json)

    return (
        optimal_pv_capacity,
        optimal_battery_capacity,
        optimal_diesel_capacity,
        optimal_dispatch,
    )


if __name__ == "__main__":
    (
        optimal_pv_capacity,
        optimal_battery_capacity,
        optimal_diesel_capacity,
        optimal_dispatch,
    ) = run(308, 2, "2024-09-12")
    print(optimal_pv_capacity)
    print(optimal_battery_capacity)
    print(optimal_diesel_capacity)

    print(optimal_dispatch.head())
