from .config import SCENARIOS
from .climate import climate_change
from .biosphere import biosphere_integrity
from .utils import multiply_list


def compute_historical_impacts(historical, historical_multiplier=1.0):
    length = len(historical['kgCO2'])
    scaled_kgco2 = [x * historical_multiplier for x in historical['kgCO2'].tolist()]
    historical_rf = climate_change(scaled_kgco2, [0] * length, [0] * length, [0] * length, [0] * length)[0]
    historical_rf_nonCO2 = multiply_list(historical_rf, 2.96)
    historical_rf_min = multiply_list(historical_rf, 1.62)
    historical_rf_max = multiply_list(historical_rf, 4.26)
    historical_bii = biosphere_integrity(historical_rf)
    historical_bii_nonCO2 = biosphere_integrity(historical_rf_nonCO2)
    historical_bii_min = biosphere_integrity(historical_rf_min)
    historical_bii_max = biosphere_integrity(historical_rf_max)
    return {
        'historical_rf': historical_rf,
        'historical_rf_nonCO2': historical_rf_nonCO2,
        'historical_rf_min': historical_rf_min,
        'historical_rf_max': historical_rf_max,
        'historical_bii': historical_bii,
        'historical_bii_nonCO2': historical_bii_nonCO2,
        'historical_bii_min': historical_bii_min,
        'historical_bii_max': historical_bii_max,
    }


def add_historical_to_impacts(dict_impacts, historical, historical_multiplier=1.0):
    h = compute_historical_impacts(historical, historical_multiplier=historical_multiplier)
    h['historical_multiplier'] = historical_multiplier
    for scenario in SCENARIOS:
        dict_impacts[scenario]['fk_historical'] = {}
        dict_impacts[scenario]['fk_historical']['RF'] = h['historical_rf'][-28:]
        dict_impacts[scenario]['fk_historical']['RFnonCO2'] = h['historical_rf_nonCO2'][-28:]
        dict_impacts[scenario]['fk_historical']['RFmin'] = h['historical_rf_min'][-28:]
        dict_impacts[scenario]['fk_historical']['RFmax'] = h['historical_rf_max'][-28:]
        dict_impacts[scenario]['fk_historical']['BItot'] = h['historical_bii'][-28:]
        dict_impacts[scenario]['fk_historical']['BItotnonCO2'] = h['historical_bii_nonCO2'][-28:]
        dict_impacts[scenario]['fk_historical']['BItotmin'] = h['historical_bii_min'][-28:]
        dict_impacts[scenario]['fk_historical']['BItotmax'] = h['historical_bii_max'][-28:]
    return dict_impacts, h
