# Order: RF, CO2atm, N, P, LSC, SOD, FWU, BIrf, BIdlu, BItot
SOS = [1, 72, 62, 9.96, 15, 4000, 10, 10, 10]
SoSOS_FHN_AeroSCOPE = [0.0088, 0.0088, 0.00016201618133512, 0.000017057109834137200, 0.00398, 0.0222, 0.00012, 0.00012, 0.00012]
SoSOS_GDP = 0.029

PB_aviation_FHN = {
    'RF': 0.0088 * 1,
    'BItot': 0.00012 * 10,
    'N': 0.00016201618133512 * 62,
    'P': 0.000017057109834137200 * 9.96,
    'RFnonCO2': 0.0088 * 1,
    'BItotnonCO2': 0.00012 * 10,
    'FWU': 0.0222 * 4000,
    'SOD': 0.00398 * 15,
    'RFmin': 0.0088 * 1,
    'RFmax': 0.0088 * 1,
    'BItotmin': 0.00012 * 10,
    'BItotmax': 0.00012 * 10,
}

PB_aviation_GDP = {
    'RF': 0.029 * 1,
    'BItot': 0.029 * 10,
    'N': 0.029 * 62,
    'P': 0.029 * 9.96,
    'FWU': 0.029 * 4000,
    'SOD': 0.029 * 15,
    'RFnonCO2': 0.029 * 1,
    'BItotnonCO2': 0.029 * 10,
    'RFmin': 0.029 * 1,
    'RFmax': 0.029 * 1,
    'BItotmin': 0.029 * 10,
    'BItotmax': 0.029 * 10,
}


def get_planetary_boundaries(method='FHN'):
    method = method.upper()
    if method == 'FHN':
        return PB_aviation_FHN
    if method == 'GDP':
        return PB_aviation_GDP
    raise ValueError("method must be 'FHN' or 'GDP'")
