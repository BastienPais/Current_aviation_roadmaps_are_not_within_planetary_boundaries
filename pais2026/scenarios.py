import numpy as np

from .config import YEARS, N_YEARS, SCENARIOS, FUEL_TYPES
from .utils import multiply_list_by_list, multiply_list_by_scalar, complement


def energy_demand(aviation_2023_mj_demand=12e12, traffic_growth=0.037, technology_improvement=0.015):
    i = 2023
    aviation_mj_prospective_demand = []
    while i < 2051:
        if i == 2023:
            aviation_mj_prospective_demand.append(aviation_2023_mj_demand)
        else:
            aviation_mj_prospective_demand.append(
                aviation_mj_prospective_demand[-1] * (1 + traffic_growth) * (1 - technology_improvement)
            )
        i += 1
    return aviation_mj_prospective_demand


def mono_ramp_up():
    interp = [i for i in range(28)]
    xp = (0, 28)
    yp = (-5, 5)
    x = np.interp(interp, xp, yp)
    z = np.exp(-x)
    sig = (1 / (1 + z)).tolist()
    return sig


def refuel_ramp_up():
    year = [i + 2023 for i in range(28)]
    refuel_x = (2023, 2025, 2030, 2032, 2035, 2040, 2045, 2050)
    ptl_y = (0, 0, 0.007, 0.012, 0.05, 0.10, 0.15, 0.35)
    bio_y = (0, 0.02, 0.053, 0.048, 0.15, 0.24, 0.27, 0.35)
    fk_y = (1, 0.98, 0.94, 0.94, 0.8, 0.66, 0.58, 0.3)
    return {
        "share_fk": (np.interp(year, refuel_x, fk_y)).tolist(),
        "share_efuels": (np.interp(year, refuel_x, ptl_y)).tolist(),
        "share_biofuels": (np.interp(year, refuel_x, bio_y)).tolist(),
        "share_lh2": [0 for _ in range(28)],
        "share_atj": 0.425,
        "share_ft": 0.425,
        "share_hefa": 0.15,
    }


def _as_list_or_repeated(value, n=N_YEARS):
    if isinstance(value, list):
        return value
    return [value for _ in range(n)]


def build_scenario(parameters, aviation_mj_prospective_demand):
    # Accept the original typo if it appears in old parameter dictionaries.
    share_ft = parameters.get("share_ft", parameters.get("sahre_ft", 0))

    share_fk = _as_list_or_repeated(parameters["share_fk"])
    share_efuels = _as_list_or_repeated(parameters["share_efuels"])
    share_biofuels = _as_list_or_repeated(parameters["share_biofuels"])
    share_lh2 = _as_list_or_repeated(parameters["share_lh2"])

    fk = multiply_list_by_list(share_fk, aviation_mj_prospective_demand)
    efuels = multiply_list_by_list(share_efuels, aviation_mj_prospective_demand)
    atj = multiply_list_by_list(multiply_list_by_scalar(share_biofuels, parameters["share_atj"]), aviation_mj_prospective_demand)
    ft = multiply_list_by_list(multiply_list_by_scalar(share_biofuels, share_ft), aviation_mj_prospective_demand)
    hefa = multiply_list_by_list(multiply_list_by_scalar(share_biofuels, parameters["share_hefa"]), aviation_mj_prospective_demand)
    lh2 = multiply_list_by_list(share_lh2, aviation_mj_prospective_demand)

    return {"fk": fk, "efuels": efuels, "atj": atj, "ft": ft, "hefa": hefa, "lh2": lh2}


def build_parameters(repartition_fuels):
    ramp = mono_ramp_up()
    return {
        "Baseline": {
            "share_fk": 1,
            "share_efuels": 0,
            "share_biofuels": 0,
            "share_lh2": 0,
            "share_atj": 0,
            "share_ft": 0,
            "share_hefa": 0,
        },
        "CR1": {
            "share_fk": repartition_fuels["S1_FK"].to_list(),
            "share_efuels": repartition_fuels["S1_efuel"].to_list(),
            "share_biofuels": repartition_fuels["S1_biofuel"].to_list(),
            "share_atj": 0.425,
            "share_ft": 0.425,
            "share_hefa": 0.15,
            "share_lh2": repartition_fuels["S1_LH2"].to_list(),
        },
        "CR2": {
            "share_fk": repartition_fuels["S2_FK"].to_list(),
            "share_efuels": repartition_fuels["S2_efuel"].to_list(),
            "share_biofuels": repartition_fuels["S2_biofuel"].to_list(),
            "share_atj": 0.425,
            "share_ft": 0.425,
            "share_hefa": 0.15,
            "share_lh2": repartition_fuels["S2_LH2"].to_list(),
        },
        "CR3": {
            "share_fk": repartition_fuels["S3_FK"].to_list(),
            "share_efuels": repartition_fuels["S3_efuel"].to_list(),
            "share_biofuels": repartition_fuels["S3_biofuel"].to_list(),
            "share_atj": 0.425,
            "share_ft": 0.425,
            "share_hefa": 0.15,
            "share_lh2": repartition_fuels["S3_LH2"].to_list(),
        },
        "CR4": refuel_ramp_up(),
        "MTS1": {
            "share_fk": complement(ramp),
            "share_efuels": [0 for _ in range(28)],
            "share_biofuels": ramp,
            "share_atj": 0.425,
            "share_ft": 0.425,
            "share_hefa": 0.15,
            "share_lh2": [0 for _ in range(28)],
        },
        "MTS2": {
            "share_fk": complement(ramp),
            "share_efuels": [0 for _ in range(28)],
            "share_biofuels": ramp,
            "share_atj": 0.15,
            "share_ft": 0.15,
            "share_hefa": 0.70,
            "share_lh2": [0 for _ in range(28)],
        },
        "MTS3": {
            "share_fk": complement(ramp),
            "share_efuels": ramp,
            "share_biofuels": [0 for _ in range(28)],
            "share_lh2": [0 for _ in range(28)],
            "share_atj": 0,
            "share_ft": 0,
            "share_hefa": 0,
        },
        "MTS4": {
            "share_fk": complement(ramp),
            "share_efuels": ramp,
            "share_biofuels": [0 for _ in range(28)],
            "share_lh2": [0 for _ in range(28)],
            "share_atj": 0,
            "share_ft": 0,
            "share_hefa": 0,
        },
    }


def build_all_scenarios(repartition_fuels, aviation_mj_prospective_demand):
    params = build_parameters(repartition_fuels)
    return {scenario: build_scenario(params[scenario], aviation_mj_prospective_demand) for scenario in SCENARIOS}


def scenario_as_list(scenarios, scenario_name):
    """Return [fk, efuels, atj, ft, hefa, lh2], matching the original notebook ordering."""
    return [scenarios[scenario_name][fuel_type] for fuel_type in FUEL_TYPES]
