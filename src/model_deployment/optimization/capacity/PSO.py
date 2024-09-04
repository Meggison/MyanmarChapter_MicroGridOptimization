"""Optimization of Battery and Solar Capacity using Particle Swarm Optimization (PSO)

notes:
* Given a load and PV generation data per unit capacity, this script optimizes the battery and solar capacity with the objective to minimize installation costs
* This is loosely based off the equations at the end of "Rural electrification through village grids - Assessing the cost
competitiveness of isolated renewable energy technologies in Indonesia": https://ethz.ch/content/dam/ethz/special-interest/gess/energy-politics-group-dam/documents/Journal%20Articles/Blum%20et%20al_2013_Renewable%20and%20Sustainable%20Energy%20Reviews.pdf
"""
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

# Constants
eta_batt = 0.8123  # Battery charging efficiency

LOAD_DATA_PATH = "./samples/Tanintharyi_13.1304_98.8394_131.csv"
PV_DATA_PATH = "./res/pv/Tanintharyi_13.1304_98.8394.csv"

load_df = pd.read_csv(LOAD_DATA_PATH)
load_df["timestamp"] = pd.to_datetime(load_df["timestamp"])
load_df.set_index("timestamp", inplace=True)
hourly_load = load_df.resample("H").first()

load_ts = hourly_load["kW"].values
pv_ts = pd.read_csv(PV_DATA_PATH)["electricity"].values

# Example load and PV generation data per unit capacity
# E_PV here represents the energy generated per unit of PV capacity over time [Wh/W]
E_load = load_ts[:48]  # Energy load over time [Wh]
E_PV = pv_ts[:48]  # Energy generated per unit PV capacity [Wh/W]
# Battery initial state of charge
battery_initial_soc = 0  # Initial state of charge


def energy_balance(PV_capacity, battery_capacity):
    """Calculate energy balance over the time period.
    PV_capacity: Total PV capacity [W]
    battery_capacity: Total battery capacity [Wh]
    """
    PV_output = PV_capacity * E_PV  # Actual energy produced by the PV system [Wh]
    E_batt = np.zeros_like(E_load)
    soc = battery_initial_soc  # State of charge starts at initial SOC

    for t in range(len(E_load)):
        surplus = PV_output[t] - E_load[t]

        if surplus > 0:
            # Charge battery with surplus
            soc += eta_batt * surplus
            soc = min(soc, battery_capacity)  # Cap at battery capacity
        else:
            # Discharge battery to meet deficit
            soc += surplus
            soc = max(soc, 0)  # SOC cannot go below 0
            E_batt[t] = -surplus if soc > 0 else 0

    return E_batt


def cost_func(x):
    """Objective function to minimize"""
    PV_capacity = x[0]
    battery_capacity = x[1]

    PV_capacity_cost = (
        PV_capacity * 5
    )  # Example cost per W for PV (replace with real data)
    battery_capacity_cost = (
        battery_capacity * 1
    )  # Example cost per Wh for battery (replace with real data)

    # Total cost
    total_cost = (PV_capacity_cost + battery_capacity_cost)
    # LCOE was not giving me good results, so I simplified it to to installation costs only
    return total_cost


# Constraints: Ensure demand is met
def demand_constraint(x):
    PV_capacity = x[0]
    battery_capacity = x[1]
    E_BAT = energy_balance(PV_capacity, battery_capacity)
    return np.min(E_BAT + PV_capacity * E_PV - E_load)


def constrained_lcoe(x):
    """Objective function that penalizes if constraints are violated"""
    constraint_violation = demand_constraint(x)
    if constraint_violation < 0:
        # Apply a large penalty if the constraint is violated
        return np.inf
    return cost_func(x)


# Initial guess for the optimization
x0 = [550, 300]  # Initial guesses for [PV capacity, Battery capacity]

bounds = [(0, 1000), (0, 5000)]  # Lower and upper bounds

# Attempt optimization with different methods or tweaks
result = differential_evolution(
    constrained_lcoe, bounds, strategy="best1bin", maxiter=1000, popsize=15, tol=1e-7
)

# Set print options for prettier output
np.set_printoptions(precision=1, suppress=True)

# Check if the optimization was successful
if result.success:
    optimal_PV_capacity = result.x[0]
    optimal_battery_capacity = result.x[1]
    print(f"Optimal PV capacity: {optimal_PV_capacity} W")
    print(f"Optimal battery capacity: {optimal_battery_capacity} W")
    print(f"Minimum Cost: {result.fun}")
    df = pd.DataFrame(
        {
            'Load': E_load,
            "Energy produced": optimal_PV_capacity * E_PV,
            "Energy balance": energy_balance(
                optimal_PV_capacity, optimal_battery_capacity
            ),
            "Load met": energy_balance(optimal_PV_capacity, optimal_battery_capacity)
            + optimal_PV_capacity * E_PV
            - E_load,
        }
    )
    # print(df.head(50))

else:
    print(f"Optimization failed: {result.message}")
    print(f"Last result: {result.x}")
