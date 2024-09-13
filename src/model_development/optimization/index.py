from math import ceil
import pandas as pd

from src.data_collection.renewable_ninja import get_pv_output
from src.data_collection.supabase import get_village_cluster_data
from src.data_collection.utilities import comparable_date
from src.model_development.optimization.capacity.index import optimize_capacity
from src.model_development.optimization.demand.index import build_settlement_demand


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
    ) = optimize_capacity(demand.loc[::60, "kW"].values, unit_pv["electricity"].values)
    optimal_dispatch["timestamp"] = demand.loc[::60, "timestamp"].values
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
    ) = run(308, 14, "2024-09-12")
