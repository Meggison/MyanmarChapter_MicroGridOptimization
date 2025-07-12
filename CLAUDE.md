# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI-driven micro-grid optimization system for rural electrification in Myanmar. The project combines demand forecasting, PV generation prediction using XGBoost, and multi-objective optimization for solar, battery, and diesel capacity planning.

## Architecture

The codebase follows a modular structure with clear separation of concerns:

- **`src/data_collection/`**: External data integration (Supabase village data, Renewables Ninja API)
- **`src/data_wrangling/`**: Data processing and transformation utilities  
- **`src/model_development/`**: Core optimization algorithms and forecasting models
  - **`optimization/`**: Main optimization engine with capacity planning and demand modeling
  - **`Micro-Grid_Operation_Optimzation/`**: MPC control simulation
- **`src/model_deployment/`**: Production API and trained models
- **`src/utils/`**: Shared utilities and helper functions
- **`notebooks/`**: Jupyter notebooks for analysis and experimentation
- **`docs/`**: Documentation and presentations
- **`reports/`**: Generated reports and outputs

## Key Components

### Main Entry Point
The primary optimization function is in `src/model_development/optimization/index.py:16` which orchestrates:
1. Village cluster data retrieval from Supabase
2. Demand forecasting using RAMP library with Myanmar-specific appliance profiles
3. PV generation forecasting using pre-trained XGBoost model
4. Capacity optimization using differential evolution algorithm

### Optimization Engine
Core optimization logic in `src/model_development/optimization/capacity/index.py:178` uses:
- Particle Swarm Optimization (PSO) via differential evolution
- Multi-objective cost minimization (CAPEX + OPEX)
- Energy balance constraints ensuring demand is always met
- Battery state-of-charge modeling with round-trip efficiency

### Demand Modeling
Settlement demand generation in `src/model_development/optimization/demand/index.py:81`:
- Uses RAMP library for stochastic appliance usage patterns
- Myanmar-specific appliance definitions and usage statistics
- Seasonal cooling demand integration from Renewables Ninja
- Monte Carlo household composition modeling

## Environment Setup

Required environment variables:
- `SUPABASE_KEY`: API key for village cluster data
- `RENEWABLES_NINJA_API_TOKEN`: Token for weather and solar data

Dependencies are managed via `src/model_development/optimization/requirements.txt`:
```
joblib==1.4.2
numpy==1.24.3
pandas==2.0.0
plotly==5.22.0
pymgrid==1.2.2
python-dotenv==1.0.1
rampdemand==0.5.2
requests==2.28.2
scipy==1.13.0
tqdm==4.65.0
```

## Running the System

### Main Optimization
Execute the full optimization pipeline:
```bash
cd src/model_development/optimization
python index.py
```

The main `run()` function accepts:
- `cluster_id`: Village cluster ID from Supabase
- `num_days`: Optimization period length
- `start_date`: Simulation start date

### Jupyter Notebooks
Key analysis notebooks in `notebooks/`:
- `grdc_analysis.ipynb`: Grid reliability and demand analysis
- `XGBoost_24hourprediction.ipynb`: PV forecasting model development
- `Micro_Grid_Simulation_Myanmar_Load_and_PV_data_With_MPC_Control.ipynb`: Full system simulation

## Model Files

Pre-trained models are stored as:
- `src/model_development/optimization/xgboost_model.json`: XGBoost PV forecasting model
- `src/model_deployment/xgboost_model.json`: Production deployment copy

## Data Sources

- **Village Data**: Supabase database with population, household, and geographic data
- **Weather Data**: Renewables Ninja API for historical PV generation and cooling demand
- **Appliance Profiles**: Myanmar-specific usage patterns from academic research

## Development Notes

- The system uses "comparable date" logic to map current dates to historical weather data
- Optimization assumes 5-year simulation period with load scaling factors
- Battery modeling includes round-trip efficiency and depth-of-discharge constraints
- Cost parameters are based on Southeast Asian microgrid studies