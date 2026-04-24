import pandas as pd

from .config import SCENARIOS
from .scenarios import scenario_as_list


def extract_lci_electricity(inventory_df):
    donnees_LCI = {}
    fuel_types = ['FK', 'efuels', 'PTLRES', 'ATJ', 'FT', 'HEFA', 'LH2']
    search_patterns = {
        'natural gas': 'electricity production, natural gas',
        'nuclear': 'electricity production, nuclear',
        'oil': 'electricity production, oil',
        'coal': 'electricity production, at hard coal|electricity production, coal',
        'wind onshore': 'electricity production, wind.*onshore',
        'wind offshore': 'electricity production, wind.*offshore',
        'photovoltaic': 'electricity production, photovoltaic',
        'hydro': 'electricity production, hydro',
        'deep geothermal': 'electricity production, deep geothermal',
        'biomass': 'electricity production, at biomass',
        'solar': 'electricity production, solar',
        'lignite': 'electricity production, at lignite|electricity production, lignite',
    }
    for fuels in fuel_types:
        donnees_LCI[fuels] = {}
        for key, pattern in search_patterns.items():
            somme = inventory_df.loc[inventory_df['name'].str.contains(pattern, case=False, regex=True), fuels].sum()
            donnees_LCI[fuels][key] = somme
    return donnees_LCI


def electricity_requirements(scenarios_data, inventory_df):
    donnees_LCI = extract_lci_electricity(inventory_df)
    dict_electricity = {'EF': {}}
    for fuel in ['FK', 'LH2', 'PTLRES', 'efuels', 'FT', 'ATJ', 'HEFA']:
        dict_electricity['EF'][fuel] = sum(donnees_LCI[fuel].values())

    for scenario in SCENARIOS:
        scenario_list = scenario_as_list(scenarios_data, scenario)
        dict_electricity[scenario] = {}
        dict_electricity[scenario]['FK'] = dict_electricity['EF']['FK'] * scenario_list[0][27]
        dict_electricity[scenario]['LH2'] = dict_electricity['EF']['LH2'] * scenario_list[5][27]
        dict_electricity[scenario]['efuels'] = dict_electricity['EF']['PTLRES' if scenario == 'MTS4' else 'efuels'] * scenario_list[1][27]
        dict_electricity[scenario]['FT'] = dict_electricity['EF']['FT'] * scenario_list[3][27]
        dict_electricity[scenario]['ATJ'] = dict_electricity['EF']['ATJ'] * scenario_list[2][27]
        dict_electricity[scenario]['HEFA'] = dict_electricity['EF']['HEFA'] * scenario_list[4][27]

    for scenario in SCENARIOS:
        for fuel_type in ['FK', 'efuels', 'ATJ', 'FT', 'HEFA', 'LH2']:
            dict_electricity[scenario][fuel_type] /= 1e12  # kWh to PWh
    return dict_electricity, donnees_LCI


def biomass_requirements(scenarios_data):
    def mj_biomasse_per_mj_fuel(calorific_value, kgbio_per_kg_fuel):
        return calorific_value * kgbio_per_kg_fuel

    dict_biomass = {}
    dict_biomass['calorific value'] = {'HEFA': 39.65, 'FT': 19.5, 'ATJ': 16.54}
    dict_biomass['kg feedstocks per MJ fuel'] = {'ATJ': 0.10191, 'FT': 0.0421, 'HEFA': 0.0175}

    for bio in ['FT', 'ATJ', 'HEFA']:
        dict_biomass[bio] = mj_biomasse_per_mj_fuel(
            dict_biomass['calorific value'][bio],
            dict_biomass['kg feedstocks per MJ fuel'][bio],
        )

    for scenario in SCENARIOS:
        scenario_list = scenario_as_list(scenarios_data, scenario)
        dict_biomass[scenario] = {}
        dict_biomass[scenario]['FT'] = dict_biomass['FT'] * scenario_list[3][27]
        dict_biomass[scenario]['ATJ'] = dict_biomass['ATJ'] * scenario_list[2][27]
        dict_biomass[scenario]['HEFA'] = dict_biomass['HEFA'] * scenario_list[4][27]

    for scenario in SCENARIOS:
        for bio in ['FT', 'ATJ', 'HEFA']:
            dict_biomass[scenario][bio] /= 1e12  # MJ to EJ
    return dict_biomass


def resource_totals(dict_electricity, dict_biomass):
    total_electricity = {scenario: sum(dict_electricity[scenario].values()) for scenario in SCENARIOS}
    total_biomass = {scenario: sum(dict_biomass[scenario].values()) for scenario in SCENARIOS}
    return total_electricity, total_biomass


def dac_results(scenarios_data):
    DAC_per_MJ_PtL = (1 / 43.15) * 1.00057 * 2.35 * 0.875 * 1.57
    return {scenario: scenario_as_list(scenarios_data, scenario)[1][27] * DAC_per_MJ_PtL * 1e-9 for scenario in SCENARIOS}


def freshwater_withdrawal(scenarios_data, freshwater_df):
    freshwater_withdrawal = {'EF': {}}
    for fuels in ['FK', 'efuels', 'PTLRES', 'ATJ', 'FT', 'HEFA', 'LH2']:
        freshwater_withdrawal['EF'][fuels] = freshwater_df[fuels].values[0]

    for scenario in SCENARIOS:
        scenario_list = scenario_as_list(scenarios_data, scenario)
        freshwater_withdrawal[scenario] = {}
        freshwater_withdrawal[scenario]['FK'] = freshwater_withdrawal['EF']['FK'] * scenario_list[0][27]
        freshwater_withdrawal[scenario]['efuels'] = freshwater_withdrawal['EF']['PTLRES' if scenario == 'MTS4' else 'efuels'] * scenario_list[1][27]
        freshwater_withdrawal[scenario]['ATJ'] = freshwater_withdrawal['EF']['ATJ'] * scenario_list[2][27]
        freshwater_withdrawal[scenario]['FT'] = freshwater_withdrawal['EF']['FT'] * scenario_list[3][27]
        freshwater_withdrawal[scenario]['HEFA'] = freshwater_withdrawal['EF']['HEFA'] * scenario_list[4][27]
        freshwater_withdrawal[scenario]['LH2'] = freshwater_withdrawal['EF']['LH2'] * scenario_list[5][27]
    return freshwater_withdrawal


def land_occupation(scenarios_data, donnees_LCI):
    heures_par_an = 365 * 24
    twh_an_mw = 1e6 / heures_par_an
    densite_surfacique_puissance = {
        'natural gas': 482.1,
        'nuclear': 240.8,
        'oil': 194.6,
        'coal': 135.1,
        'wind onshore': 2.02,
        'wind offshore': 2.63,
        'photovoltaic': 6.63,
        'hydro': 0.14,
        'deep geothermal': 2.24,
        'biomass': 0.08,
        'solar': 9.70,
        'lignite': 96.10,
    }

    pennycress_oil_yield = 565
    pennycress_oil_density = 898 / 1000
    pennycress_oil_yield_kg_per_km2 = pennycress_oil_yield * pennycress_oil_density * 100
    wood_average_density = 600
    forest_volume_productivity = 4.6
    forest_mass_productivity_kg_per_km2 = forest_volume_productivity * wood_average_density * 100
    sawdust_yield = 0

    biomass = {'FT': forest_mass_productivity_kg_per_km2, 'HEFA': pennycress_oil_yield_kg_per_km2, 'ATJ': sawdust_yield}
    land_occupation_biomass = {
        'FT': 0.0421 / biomass['FT'],
        'HEFA': 0.021 / biomass['HEFA'],
        'ATJ': 0,
        'FK': 0,
        'efuels': 0,
        'LH2': 0,
    }

    for scenario in SCENARIOS:
        scenario_list = scenario_as_list(scenarios_data, scenario)
        land_occupation_biomass[scenario] = {
            'FK': land_occupation_biomass['FK'] * scenario_list[0][27],
            'efuels': land_occupation_biomass['efuels'] * scenario_list[1][27],
            'ATJ': land_occupation_biomass['ATJ'] * scenario_list[2][27],
            'FT': land_occupation_biomass['FT'] * scenario_list[3][27],
            'HEFA': land_occupation_biomass['HEFA'] * scenario_list[4][27],
            'LH2': land_occupation_biomass['LH2'] * scenario_list[5][27],
        }

    land_occupation_electricity = {'EF': {}}
    for fuels in ['FK', 'efuels', 'PTLRES', 'ATJ', 'FT', 'HEFA', 'LH2']:
        somme = 0
        for keys in densite_surfacique_puissance:
            somme = somme + donnees_LCI[fuels][keys] * 1e-9 * (twh_an_mw / densite_surfacique_puissance[keys])
        land_occupation_electricity['EF'][fuels] = somme

    for scenario in SCENARIOS:
        scenario_list = scenario_as_list(scenarios_data, scenario)
        land_occupation_electricity[scenario] = {
            'FK': land_occupation_electricity['EF']['FK'] * scenario_list[0][27],
            'efuels': land_occupation_electricity['EF']['PTLRES' if scenario == 'MTS4' else 'efuels'] * scenario_list[1][27],
            'ATJ': land_occupation_electricity['EF']['ATJ'] * scenario_list[2][27],
            'FT': land_occupation_electricity['EF']['FT'] * scenario_list[3][27],
            'HEFA': land_occupation_electricity['EF']['HEFA'] * scenario_list[4][27],
            'LH2': land_occupation_electricity['EF']['LH2'] * scenario_list[5][27],
        }

    total_land_occupation = {
        scenario: (sum(land_occupation_biomass[scenario].values()) + sum(land_occupation_electricity[scenario].values())) * 1e-6
        for scenario in SCENARIOS
    }
    return land_occupation_biomass, land_occupation_electricity, total_land_occupation
