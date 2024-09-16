# execution note and other notes
# launch over terminal via
# uvicorn main_working:app --reload
# to load the interative interface to add/see respose http://127.0.0.1:8000/docs
#pip3 install xgboost
#pip3 install uvicorm
#pip3 install fastapi

'''
Sample Input REST API
{
  "cluster_id": 308,
  "num_days": 14,
  "start_date": "2024-09-12"
}
'''

from math import ceil
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from src.data_collection.renewable_ninja import get_pv_output
from src.data_collection.supabase import get_village_cluster_data
from src.data_collection.utilities import comparable_date
from src.model_development.optimization.capacity.index import optimize_capacity
from src.model_development.optimization.demand.index import build_settlement_demand
from fastapi import FastAPI
from pydantic import BaseModel, Json
from joblib import load
import xgboost as xgb


# input request class
class data_from_frontend(BaseModel):
    cluster_id: int
    num_days: int
    start_date: str

# forecast response class
class microgrid_control_response(BaseModel):
    response_optimal_pv_capacity: float
    response_optimal_battery_capacity: float
    response_optimal_diesel_capacity: float
    response_optimal_dispatch: Json

app = FastAPI()


@app.post("/microgrid_control_ouput", response_model=microgrid_control_response)
def run(input_village_data:data_from_frontend):
    """
    cluster_id: int,
    num_days: int,
    start_date: str = pd.Timestamp.now().strftime("%Y-%m-%d"),

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
    cluster = get_village_cluster_data(input_village_data.cluster_id)
    households = ceil((cluster["Pop"] / cluster["NumPeoplePerHH"]))
    lon = cluster["X_deg"]
    lat = cluster["Y_deg"]
    demand = build_settlement_demand(
        num_households=households,
        date_start=input_village_data.start_date,
        num_days=input_village_data.num_days,
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
    optimal_dispatch_json = optimal_dispatch.to_json(orient="records")

    return microgrid_control_response(response_optimal_pv_capacity=optimal_pv_capacity,
        response_optimal_battery_capacity=optimal_battery_capacity,
        response_optimal_diesel_capacity=optimal_diesel_capacity, 
        response_optimal_dispatch=optimal_dispatch_json) 

