YEARS = list(range(2023, 2051))
N_YEARS = len(YEARS)

SCENARIOS = ["Baseline", "CR1", "CR2", "CR3", "CR4", "MTS1", "MTS2", "MTS3", "MTS4"]
FUEL_TYPES = ["fk", "efuels", "atj", "ft", "hefa", "lh2"]
FUEL_TYPES_WITH_HISTORICAL = ["fk_historical", "fk", "efuels", "atj", "ft", "hefa", "lh2"]

PBs_AESA = [
    "RF", "BItot", "N", "P", "FWU", "SOD",
    "RFmin", "RFmax", "BItotmin", "BItotmax", "RFnonCO2", "BItotnonCO2",
]

PBs_EXPORT = [
    "RF", "BItot", "N", "P", "FWU", "SOD",
    "RFnonCO2", "BItotnonCO2", "RFmin", "RFmax", "BItotmin", "BItotmax",
]

EFs_BASE = ["N", "P", "FWU", "SOD", "BIIDLU", "CO2", "CO2nonfossil", "CO2capture", "CH4", "N2O"]
EFs_WITH_VARIANTS = EFs_BASE + ["CO2min", "CO2max", "CO2nonCO2"]
