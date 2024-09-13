"""Optimization of Battery and Solar Capacity using Particle Swarm Optimization (PSO)

notes:
* Given a load and PV generation data per unit capacity, this script optimizes the battery and solar capacity with the objective to minimize installation costs
* This is loosely based off the equations at the end of "Rural electrification through village grids - Assessing the cost
competitiveness of isolated renewable energy technologies in Indonesia": https://ethz.ch/content/dam/ethz/special-interest/gess/energy-politics-group-dam/documents/Journal%20Articles/Blum%20et%20al_2013_Renewable%20and%20Sustainable%20Energy%20Reviews.pdf

studies:
* Minigrids in the Money: https://rmi.org/insight/minigrids-money/
    - lifetime: 20 years
    - diesel fuel: $0.8/L
    - diesel capex: $1050/kW
    - pv capex: $1020/kW
    - battery capex: $437/kW
* Assessing the cost competitiveness of isolated renewable energy technologies in Indonesia: https://ethz.ch/content/dam/ethz/special-interest/gess/energy-politics-group-dam/documents/Journal%20Articles/Blum%20et%20al_2013_Renewable%20and%20Sustainable%20Energy%20Reviews.pdf
    - lifetime: 20 years (diesel), 25 years (pv), 5 years (battery)
    - diesel capex: $482/kW
* Technoeconomic Assessment of Microgrids in Myanmar: https://www.eria.org/uploads/media/ERIA_DP_2018_05.pdf
    - lifetime: 20 years (diesel), 30 years (pv), 7-11 years (battery)
    - diesel capex: $490/kW
    - diesel opex: $0.026/kW
    - pv capex: $2707/kW - $1600/kW
    - pv opex: 1% capex - $10/kW
    - battery capex: $286/kW - $124/kW
    - battery opex: $0 - $0.04/kW
* World Energy Outlook: https://iea.blob.core.windows.net/assets/86ede39e-4436-42d7-ba2a-edf61467e070/WorldEnergyOutlook2023.pdf
    - pv capex: $720/kW (china)


1 liter of diesel fuel = 38 MJ OR 10kWh: https://www.bts.gov/content/energy-consumption-mode-transportation-0#:~:text=Diesel%20motor%20fuel%20%3D%2038%2C290%20kJ%2Fliter.
liters required per kWh = 1 kWh / (EFFICIENCY * 10kwh)
cost per kWh = liters required per kWh * diesel price per liter

diesel price SE Asia: https://www.rhinocarhire.com/World-Fuel-Prices.aspx ~0.97 euros/L
diesel price MYANMAR: https://www.globalpetrolprices.com/Burma-Myanmar/diesel_prices/ ~0.83$/L


"""

import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

SIMULATION_YEARS = 5

# Battery Constants
RTE_BATT = 0.95  # round trip efficiency of the battery
CHARGE_EFFICIENCY = RTE_BATT**0.5  # used for both charge and discharge
MAX_DISCHARGE = 0.9  # Maximum discharge of the battery
BATTERY_COST = 140
battery_initial_soc = 1  # Initial state of charge

# PV Constants
PV_COST = 720

# Diesel Constants
DIESEL_COST = 261
DIESEL_FUEL = 0.2

# Example load and PV generation data per unit capacity
# E_PV here represents the energy generated per unit of PV capacity over time [kWh/kW]
hours = 24 * 7 * 4 * 3
# E_load = load_ts[:hours]  # Energy load over time [kWh]
# E_PV = pv_ts[: len(E_load)]  # Energy generated per unit PV capacity [kWh/kW]


def energy_balance(pv_capacity, battery_capacity, diesel_capacity, E_load, E_PV):
    """Calculate energy balance over the time period.

    Args:
        pv_capacity (float): PV capacity [kW]
        battery_capacity (float): Battery capacity [kW]

    Returns:
        E_batt (np.array): Battery energy balance [Wh]
    """
    PV_output = pv_capacity * E_PV  # Actual energy produced by the PV system [Wh]
    E_batt = np.zeros_like(E_load)
    C_batt = np.zeros_like(E_load)
    E_diesel = np.zeros_like(E_load)
    # State of charge starts at initial SOC
    soc = battery_initial_soc * battery_capacity
    max_battery_discharge = (1 -MAX_DISCHARGE) * battery_capacity
    for t in range(len(E_load)):
        surplus = PV_output[t] - E_load[t]

        if surplus > 0:
            # Charge battery with surplus
            soc += CHARGE_EFFICIENCY * surplus
            soc = min(soc, battery_capacity)  # Cap at battery capacity
        else:
            # Discharge battery to meet deficit
            available = soc - max_battery_discharge
            discharged = min(available, -surplus / CHARGE_EFFICIENCY)
            if discharged > 0:
                soc -= discharged
            final_discharge = discharged * CHARGE_EFFICIENCY
            E_batt[t] = max(final_discharge, 0)
            surplus += final_discharge

        if surplus < -0.0000001:
            E_diesel[t] = min(-surplus, diesel_capacity)
        C_batt[t] = soc

    return E_batt, E_diesel, C_batt


def cost_func(x, E_load, E_PV):
    """Objective function to minimize.

    Args:
        x (np.array): Battery and PV capacity [kW]

    Returns:
        float: Total cost
    """
    pv_capacity = x[0]
    battery_capacity = x[1]
    diesel_capacity = x[2]

    pv_capacity_cost = pv_capacity * PV_COST
    battery_capacity_cost = battery_capacity * BATTERY_COST
    diesel_capacity_cost = diesel_capacity * DIESEL_COST

    # levelized cost of energy (LCOE)
    _, E_diesel, _ = energy_balance(
        pv_capacity, battery_capacity, diesel_capacity, E_load, E_PV
    )
    # the cost of renewable energy will not be immediately visible with few demand observations
    # so we need to scale the demand with a load factor to see the long term benefit
    # otherwise it will pick full conventional generation and not the renewable energy
    adjusted_demand = SIMULATION_YEARS * 8760
    load_factor = 1 / (len(E_load) / adjusted_demand)
    total_cost = (
        pv_capacity_cost
        + battery_capacity_cost
        + diesel_capacity_cost
        + np.sum(E_diesel * load_factor * DIESEL_FUEL)
    )
    return total_cost / np.sum(E_load * load_factor)


# Constraints: Ensure demand is met
def demand_constraint(x, E_load, E_PV):
    """Checks if the demand is met.
    Args:
        x (np.array): Battery and PV capacity [kW]

    Returns:
        float: Total cost
    """
    pv_capacity = x[0]
    battery_capacity = x[1]
    diesel_capacity = x[2]
    E_BAT, E_diesel, _ = energy_balance(
        pv_capacity, battery_capacity, diesel_capacity, E_load, E_PV
    )
    return np.min(E_BAT + E_diesel + pv_capacity * E_PV - E_load)


def constrained_cost(x, E_load, E_PV):
    """Objective function that penalizes if constraints are violated.
    Args:
        x (np.array): Battery and PV capacity [kW]

    Returns:
        float: Total cost
    """
    E_load_arr = np.array(E_load)
    E_PV_arr = np.array(E_PV)
    constraint_violation = demand_constraint(x, E_load_arr, E_PV_arr)
    if constraint_violation < -0.0001:
        # Apply a large penalty if the constraint is violated
        return np.inf
    return cost_func(x, E_load_arr, E_PV_arr)


def optimize_capacity(E_load, E_PV):
    bounds = [(0, 1000), (0, 5000), (0, 1000)]  # Lower and upper bounds

    # Attempt optimization with different methods or tweaks
    result = differential_evolution(
        constrained_cost,
        bounds,
        args=(tuple(E_load), tuple(E_PV)),
        maxiter=5000,
        popsize=15,
        tol=1e-7,
        workers=-1,
    )

    # Check if the optimization was successful
    if result.success:
        optimal_pv_capacity = result.x[0]
        optimal_battery_capacity = result.x[1]
        optimal_diesel_capacity = result.x[2]
        print(f"Optimal pv capacity: {optimal_pv_capacity} kW")
        print(f"Optimal battery capacity: {optimal_battery_capacity} kW")
        print(f"Optimal diesel capacity: {optimal_diesel_capacity} kW")
        print(f"Minimum Cost: {result.fun}")
        E_Batt, E_diesel, C_batt = energy_balance(
            optimal_pv_capacity,
            optimal_battery_capacity,
            optimal_diesel_capacity,
            E_load,
            E_PV,
        )
        df = pd.DataFrame(
            {
                "E_PV": optimal_pv_capacity * E_PV,
                "E_Batt": E_Batt,
                "E_diesel": E_diesel,
                "C_batt": C_batt,
                "E_load": E_load,
            }
        )
        return (
            optimal_pv_capacity,
            optimal_battery_capacity,
            optimal_diesel_capacity,
            df,
        )

    else:
        raise ValueError("Optimization failed")
