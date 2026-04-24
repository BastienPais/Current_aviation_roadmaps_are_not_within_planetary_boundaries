from pathlib import Path
import pandas as pd

from .scenarios import energy_demand, build_all_scenarios
from .impacts import build_impact_dict
from .historical import add_historical_to_impacts
from .aesa import compute_aesa, extract_2050_results, non_co2_factors
from .resources import electricity_requirements, biomass_requirements, resource_totals, dac_results, freshwater_withdrawal, land_occupation


def run_pipeline(
    data_dir='data',
    repartition_file='0_ICAO and ATAG fuel repartition data.xlsx',
    impacts_file='1_Impact_per_MJ_CC_selection.xlsx',
    historical_file='21_Data_Lee.xlsx',
    method='FHN',
    traffic_growth=0.037,
    efficiency_gain=0.015,
    historical_multiplier=1.0,
    include_historical=True,
    include_resources=False,
    inventory_file='3_Inventory_technosphere_CC_selection.xlsx',
    freshwater_file='5_Freshwater_withdrawal_CC_selection.xlsx',
):
    data_dir = Path(data_dir)
    repartition = pd.read_excel(data_dir / repartition_file)
    impacts = pd.read_excel(data_dir / impacts_file)
    historical = pd.read_excel(data_dir / historical_file)

    demand = energy_demand(traffic_growth=traffic_growth, technology_improvement=efficiency_gain)
    scenarios = build_all_scenarios(repartition, demand)
    dict_impacts = build_impact_dict(scenarios, impacts)

    historical_results = None
    if include_historical:
        dict_impacts, historical_results = add_historical_to_impacts(
            dict_impacts,
            historical,
            historical_multiplier=historical_multiplier,
        )
    else:
        dict_impacts, historical_results = add_historical_to_impacts(
            dict_impacts,
            historical,
            historical_multiplier=0.0,
        )

    dict_aesa = compute_aesa(dict_impacts, method=method)
    df_2050 = extract_2050_results(dict_aesa)
    df_factors = non_co2_factors(dict_aesa)

    results = {
        'demand': demand,
        'scenarios': scenarios,
        'dict_impacts': dict_impacts,
        'historical_results': historical_results,
        'parameters': {
            'traffic_growth': traffic_growth,
            'efficiency_gain': efficiency_gain,
            'historical_multiplier': historical_multiplier if include_historical else 0.0,
            'include_historical': include_historical,
            'method': method,
            'impacts_file': impacts_file,
        },
        'dict_aesa': dict_aesa,
        'df_2050': df_2050,
        'df_factors': df_factors,
    }

    if include_resources:
        inventory = pd.read_excel(data_dir / inventory_file)
        freshwater_df = pd.read_excel(data_dir / freshwater_file)
        dict_electricity, lci_electricity = electricity_requirements(scenarios, inventory)
        dict_biomass = biomass_requirements(scenarios)
        total_electricity, total_biomass = resource_totals(dict_electricity, dict_biomass)
        land_biomass, land_electricity, total_land = land_occupation(scenarios, lci_electricity)
        results.update({
            'dict_electricity': dict_electricity,
            'lci_electricity': lci_electricity,
            'dict_biomass': dict_biomass,
            'total_electricity': total_electricity,
            'total_biomass': total_biomass,
            'dac_results': dac_results(scenarios),
            'freshwater_withdrawal': freshwater_withdrawal(scenarios, freshwater_df),
            'land_occupation_biomass': land_biomass,
            'land_occupation_electricity': land_electricity,
            'total_land_occupation': total_land,
        })

    return results


def export_core_results(results, output_dir='outputs', prefix='AESA'):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results['df_2050'].to_excel(output_dir / f'{prefix}_2050_results.xlsx')
    results['df_factors'].to_excel(output_dir / f'{prefix}_non_CO2_factors.xlsx', index=False)
