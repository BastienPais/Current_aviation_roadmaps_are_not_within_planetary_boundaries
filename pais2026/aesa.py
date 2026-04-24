import numpy as np
import pandas as pd

from .config import SCENARIOS, FUEL_TYPES, FUEL_TYPES_WITH_HISTORICAL, PBs_AESA, PBs_EXPORT
from .downscaling import get_planetary_boundaries


def compute_aesa(dict_impacts, method='FHN'):
    PB_aviation = get_planetary_boundaries(method)
    dict_AESA = {}
    stock_PBs = ['RF', 'BItot', 'RFnonCO2', 'BItotnonCO2', 'RFmin', 'RFmax', 'BItotmin', 'BItotmax']

    for scenario in SCENARIOS:
        dict_AESA[scenario] = {}
        dict_AESA[scenario]['fk_historical'] = {}

        for fuel_type in FUEL_TYPES:
            dict_AESA[scenario][fuel_type] = {}
            for PB in PBs_AESA:
                dict_AESA[scenario][fuel_type][PB] = []
                for i in range(28):
                    dict_AESA[scenario][fuel_type][PB].append(dict_impacts[scenario][fuel_type][PB][i] / PB_aviation[PB])
                dict_AESA[scenario]['fk_historical'][PB] = [0] * 28

        for stock_PB in stock_PBs:
            for i in range(28):
                dict_AESA[scenario]['fk_historical'][stock_PB][i] = dict_impacts[scenario]['fk_historical'][stock_PB][i] / PB_aviation[stock_PB]

    return dict_AESA


def extract_2050_values(dict_AESA):
    dict_AESA_27th_values = {
        scenario: {
            fuel_type: {PB: dict_AESA[scenario][fuel_type][PB][27] for PB in PBs_EXPORT}
            for fuel_type in FUEL_TYPES_WITH_HISTORICAL
        }
        for scenario in SCENARIOS
    }

    for scenario in SCENARIOS:
        dict_AESA_27th_values[scenario]['total'] = {}
        for PB in PBs_EXPORT:
            dict_AESA_27th_values[scenario]['total'][PB] = sum(
                dict_AESA_27th_values[scenario][fuel_type][PB]
                for fuel_type in FUEL_TYPES_WITH_HISTORICAL
            )
    return dict_AESA_27th_values


def extract_2050_results(dict_AESA):
    values = extract_2050_values(dict_AESA)
    df = pd.DataFrame.from_dict(
        {(scenario, fuel_type): values[scenario][fuel_type] for scenario in values for fuel_type in values[scenario]},
        orient='index',
    )
    df.index = pd.MultiIndex.from_tuples(df.index, names=['scenario', 'fuel_type'])
    return df


def non_co2_factors(dict_AESA):
    values = extract_2050_values(dict_AESA)
    facteurs = []
    for scenario in SCENARIOS:
        total = values[scenario]['total']['BItot']
        nonCO2 = values[scenario]['total']['BItotnonCO2']
        min_ = values[scenario]['total']['BItotmin']
        max_ = values[scenario]['total']['BItotmax']
        facteurs.append({
            'scenario': scenario,
            'facteur_nonCO2': nonCO2 / total if total else np.nan,
            'facteur_min': min_ / total if total else np.nan,
            'facteur_max': max_ / total if total else np.nan,
        })
    return pd.DataFrame(facteurs)
