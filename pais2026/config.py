YEARS = list(range(2023, 2051))
N_YEARS = len(YEARS)

SCENARIOS = ["Baseline", "CR1", "CR2", "CR3", "CR4", "MTS1", "MTS2", "MTS3", "MTS4"]
FUEL_TYPES = ["fk", "efuels", "atj", "ft", "hefa", "lh2"]
FUEL_TYPES_WITH_HISTORICAL = ["fk_historical", "fk", "efuels", "atj", "ft", "hefa", "lh2"]

PBs_AESA = [
    "RF", "BItot", "N", "P", "FWU", "SOD",
]

PBs_EXPORT = [
    "RF", "BItot", "N", "P", "FWU", "SOD",
]

EFs_BASE = ["N", "P", "FWU", "SOD", "BIIDLU", "CO2", "CO2nonfossil", "CO2capture", "CH4", "N2O"]
