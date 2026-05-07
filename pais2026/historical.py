from .config import SCENARIOS
from .climate import climate_change
from .biosphere import biosphere_integrity
from .utils import multiply_list


def compute_historical_impacts(historical, historical_multiplier=1.0):
    length = len(historical['kgCO2'])
    scaled_kgco2 = [x * historical_multiplier for x in historical['kgCO2'].tolist()]
    historical_rf = climate_change(scaled_kgco2, [0] * length, [0] * length, [0] * length, [0] * length)[0]
    historical_bii = biosphere_integrity(historical_rf)
    return {
        'historical_rf': historical_rf,
        'historical_bii': historical_bii,
    }


def add_historical_to_impacts(dict_impacts, historical, historical_multiplier=1.0):
    h = compute_historical_impacts(historical, historical_multiplier=historical_multiplier)
    h['historical_multiplier'] = historical_multiplier
    for scenario in SCENARIOS:
        dict_impacts[scenario]['fk_historical'] = {}
        dict_impacts[scenario]['fk_historical']['RF'] = h['historical_rf'][-28:]
        dict_impacts[scenario]['fk_historical']['BItot'] = h['historical_bii'][-28:]
    return dict_impacts, h
