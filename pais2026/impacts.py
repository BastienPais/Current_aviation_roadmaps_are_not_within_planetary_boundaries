from .config import SCENARIOS, FUEL_TYPES, EFs_BASE
from .climate import climate_change
from .biosphere import biosphere_integrity
from .utils import sum_two_lists


def extract_emission_factors(impacts):
    dictionnaire_EF = {}
    for EF in EFs_BASE:
        colonnes_EF = [colonne for colonne in impacts.columns if colonne.startswith(f"{EF}_")]
        for colonne in colonnes_EF:
            nom_fuel = colonne.split('_')[1]
            donnees = impacts[colonne].tolist()
            if nom_fuel not in dictionnaire_EF:
                dictionnaire_EF[nom_fuel] = {}
            dictionnaire_EF[nom_fuel][EF] = donnees

    for fuel in dictionnaire_EF:
        if 'CO2' in dictionnaire_EF[fuel]:
            co2_values = dictionnaire_EF[fuel]['CO2']
    return dictionnaire_EF


def impact_factor_index(i):
    """Preserves the original temporal logic:
    2023-2029 -> EF row 0; 2030-2039 -> row 1; 2040-2049 -> row 2; 2050 -> row 3.
    """
    if i < 7:
        return 0
    elif i < 17:
        return 1
    elif i < 27:
        return 2
    else:
        return 3


def _fuel_source_name(scenario, fuel_type):
    if fuel_type == 'fk':
        return 'FK'
    if fuel_type == 'efuels':
        return 'PTLRES' if scenario == 'MTS4' else 'PTLWG'
    if fuel_type == 'atj':
        return 'ATJ'
    if fuel_type == 'ft':
        return 'FT'
    if fuel_type == 'hefa':
        return 'HEFA'
    if fuel_type == 'lh2':
        return 'LH2'
    raise KeyError(f"Unknown fuel_type: {fuel_type}")


def build_impact_dict(scenarios_data, impacts):
    dictionnaire_EF = extract_emission_factors(impacts)
    dict_impacts = {}

    for scenario in SCENARIOS:
        dict_impacts[scenario] = {}
        for fuel_type in FUEL_TYPES:
            fuel_values = scenarios_data[scenario][fuel_type]
            dict_impacts[scenario][fuel_type] = {PB: [] for PB in EFs_WITH_VARIANTS}
            source = _fuel_source_name(scenario, fuel_type)

            for PB in EFs_WITH_VARIANTS:
                for i, fuel_amount in enumerate(fuel_values):
                    # IMPORTANT: this keeps the original notebook logic.
                    # if i < 7: 2023-2029 use factor 0
                    # elif i < 17: 2030-2039 use factor 1
                    # elif i < 27: 2040-2049 use factor 2
                    # else: 2050 use factor 3
                    if i < 7:
                        ef_index = 0
                    elif i < 17:
                        ef_index = 1
                    elif i < 27:
                        ef_index = 2
                    else:
                        ef_index = 3
                    dict_impacts[scenario][fuel_type][PB].append(dictionnaire_EF[source][PB][ef_index] * fuel_amount)

    return add_dynamic_impacts(dict_impacts)


def add_dynamic_impacts(dict_impacts):
    for scenario in SCENARIOS:
        for fuel_type in FUEL_TYPES:
            rf_values = climate_change(
                dict_impacts[scenario][fuel_type]['CO2'],
                dict_impacts[scenario][fuel_type]['CO2nonfossil'],
                dict_impacts[scenario][fuel_type]['CO2capture'],
                dict_impacts[scenario][fuel_type]['CH4'],
                dict_impacts[scenario][fuel_type]['N2O'],
            )[0]
            rf_nonCO2_values = climate_change(
                dict_impacts[scenario][fuel_type]['CO2nonCO2'],
                dict_impacts[scenario][fuel_type]['CO2nonfossil'],
                dict_impacts[scenario][fuel_type]['CO2capture'],
                dict_impacts[scenario][fuel_type]['CH4'],
                dict_impacts[scenario][fuel_type]['N2O'],
            )[0]
            rf_min_values = climate_change(
                dict_impacts[scenario][fuel_type]['CO2min'],
                dict_impacts[scenario][fuel_type]['CO2nonfossil'],
                dict_impacts[scenario][fuel_type]['CO2capture'],
                dict_impacts[scenario][fuel_type]['CH4'],
                dict_impacts[scenario][fuel_type]['N2O'],
            )[0]
            rf_max_values = climate_change(
                dict_impacts[scenario][fuel_type]['CO2max'],
                dict_impacts[scenario][fuel_type]['CO2nonfossil'],
                dict_impacts[scenario][fuel_type]['CO2capture'],
                dict_impacts[scenario][fuel_type]['CH4'],
                dict_impacts[scenario][fuel_type]['N2O'],
            )[0]

            dict_impacts[scenario][fuel_type]['RF'] = rf_values
            dict_impacts[scenario][fuel_type]['BIrf'] = biosphere_integrity(dict_impacts[scenario][fuel_type]['RF'])
            dict_impacts[scenario][fuel_type]['BItot'] = sum_two_lists(dict_impacts[scenario][fuel_type]['BIrf'], dict_impacts[scenario][fuel_type]['BIIDLU'])
    return dict_impacts
