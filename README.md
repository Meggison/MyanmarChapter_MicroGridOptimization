## Microgrid Optimization for Rural Electrification in Myanmar

An advanced machine learning framework for sustainable rural electrification in Myanmar, combining renewable energy forecasting, demand modeling, and multi-objective capacity optimization.

Link to the main repository on DagsHub [here](https://dagshub.com/Omdena/MyanmarChapter_MicroGridOptimization)

## Project Overview

This project develops an intelligent microgrid optimization system specifically designed for Myanmar's rural electrification challenges. By leveraging AI-driven forecasting models and sophisticated optimization algorithms, the system determines optimal configurations for solar PV, battery storage, and diesel generators to provide reliable and cost-effective electricity access.

## Key Achievements

### Forecasting Models Performance
- **Prophet Model**: 91.8% accuracy (R² = 0.918) for 24-hour solar generation forecasting
- **XGBoost Model**: 91.3% accuracy (R² = 0.913) with excellent out-of-time performance
- **LSTM Model**: 70.22% accuracy with deep learning approach
- **SARIMA Model**: 49.6% accuracy with traditional time series methods

### System Optimization Results
- **100% Load Coverage**: Zero loss of load events in simulation
- **Optimal Resource Allocation**: Efficient PV-battery-diesel hybrid systems
- **Cost Minimization**: LCOE-optimized capacity planning
- **Renewable Integration**: High renewable energy penetration with minimal curtailment

### Data Analysis Insights
- **Population Coverage**: Analysis of 303,758 population clusters nationwide
- **Investment Analysis**: Region-specific cost projections for 2020-2030
- **Hydropower Potential**: 45+ years of water discharge data across 7 river stations
- **Seasonal Patterns**: Comprehensive understanding of Myanmar's energy demand cycles

## Technical Architecture

### Core Components
- **Data Collection**: Supabase integration, Renewables Ninja API
- **Demand Modeling**: RAMP-based stochastic appliance usage simulation
- **Generation Forecasting**: Multi-model ensemble with XGBoost and Prophet
- **Capacity Optimization**: Differential evolution algorithm with energy balance constraints
- **System Simulation**: MPC-controlled microgrid operation

### Key Features
- Myanmar-specific appliance usage patterns and demographics
- Weather-dependent seasonal demand modeling
- Real-time optimization with battery state-of-charge constraints
- Cost-optimized CAPEX/OPEX minimization
- Scalable village cluster analysis framework

## Results & Impact

### Model Performance Comparison
| Model | RMSE (kW) | MAE (kW) | R² Score | Accuracy |
|-------|-----------|----------|----------|----------|
| Prophet | 0.067 | 0.049 | 0.918 | 91.8% |
| XGBoost | 0.070 | 0.037 | 0.913 | 91.3% |
| LSTM | 3.90 | 2.48 | - | 70.2% |
| SARIMA | 0.168 | 0.091 | 0.496 | 49.6% |

### Regional Electrification Analysis
- **Highest Investment Regions**: Bago, Ayeyawaddy, Yangon
- **Average Demand**: 308.8 kWh/capita/year
- **Renewable Potential**: Significant solar and hydropower resources identified

### System Configuration Optimization
- **Battery Efficiency**: 95% round-trip efficiency modeling
- **Diesel Backup**: Cost-optimal sizing for reliability
- **PV Capacity**: Weather-adjusted generation profiles
- **Load Forecasting**: Village-scale demand prediction

## Repository Structure

```
├── src/
│   ├── data_collection/          # External API integrations
│   ├── data_wrangling/           # Data preprocessing utilities
│   ├── model_development/        # Optimization and forecasting
│   │   └── optimization/         # Core optimization engine
│   ├── model_deployment/         # Production APIs
│   └── utils/                    # Shared utilities
├── notebooks/                    # Analysis and experimentation
│   ├── LSTM_FORECASTING.ipynb
│   ├── XGBoost_24hourprediction.ipynb
│   ├── PROPHET.ipynb
│   ├── SARIMA.ipynb
│   └── grdc_analysis.ipynb
├── docs/                         # Documentation
```

## Quick Start

### Prerequisites
```bash
pip install -r src/model_development/optimization/requirements.txt
```

### Environment Variables
```bash
export SUPABASE_KEY="your_supabase_api_key"
export RENEWABLES_NINJA_API_TOKEN="your_renewables_ninja_token"
```

### Run Optimization
```python
from src.model_development.optimization.index import run

# Optimize microgrid for village cluster 308 over 2 days
optimal_pv, optimal_battery, optimal_diesel, dispatch = run(
    cluster_id=308, 
    num_days=2, 
    start_date="2024-09-12"
)
```

## Key Findings

1. **Renewable Energy Viability**: High solar generation potential across Myanmar with predictable seasonal patterns
2. **Optimal System Design**: Hybrid PV-battery-diesel systems provide most cost-effective solution
3. **Forecasting Accuracy**: Machine learning models achieve >90% accuracy for generation prediction
4. **Investment Priorities**: Data-driven identification of high-impact regions for electrification
5. **Technical Feasibility**: MPC-controlled microgrids demonstrate reliable operation under varying conditions

## Methodology

### Demand Modeling
- Stochastic appliance usage simulation based on Myanmar household surveys
- Seasonal cooling demand integration from weather data
- Village-scale aggregation with realistic household compositions

### Generation Forecasting
- Multi-model ensemble approach for robust predictions
- Feature engineering with weather variables and lag features
- Out-of-time validation for real-world performance assessment

### Capacity Optimization
- Multi-objective optimization balancing cost and reliability
- Energy balance constraints ensuring 100% load coverage
- Battery state-of-charge modeling with efficiency losses

## Impact & Applications

This framework provides a replicable methodology for:
- **Policy Planning**: Evidence-based electrification strategies
- **Investment Decisions**: Risk-adjusted capacity planning
- **System Design**: Optimal microgrid configurations
- **Resource Assessment**: Renewable energy potential mapping

## Contributing

Contributions welcome! This project demonstrates sustainable electrification approaches applicable across Southeast Asia and similar developing regions.
