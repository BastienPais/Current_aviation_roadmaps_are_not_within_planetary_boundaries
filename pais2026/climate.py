import math
import numpy as np

# Carbon dioxide
a0 = 0.212
a1 = 0.244
a2 = 0.336
a3 = 0.207
alpha1 = 336.4
alpha2 = 27.89
alpha3 = 4.055
molar_mass_CO2 = 44.01
molar_mass_CO2_nonfossil = 44.01
molar_mass_CO2_capture = 44.01
sens_RF_CO2 = 5.35
CO2_atmospheric_concentration_2019 = 410  # ppm

# Methane
alpha_methane = 12.4
molar_mass_CH4 = 16.04
beta_methane = 0.036
CH4_atmospheric_concentration_2019 = 1866  # ppb

# Dinitrogen monoxide
alpha_N2O = 121
molar_mass_N2O = 44.01
beta_N2O = 0.12
N2O_atmospheric_concentration_2019 = 332  # ppb

# Other
molar_mass_air = 28.97


def fraction_calculation():
    fr_CO2 = []
    fr_CH4 = []
    fr_N2O = []
    for i in range(0, 150):
        fr_CO2.append(a0 + a1 * math.exp(-i / alpha1) + a2 * math.exp(-i / alpha2) + a3 * math.exp(-i / alpha3))
        fr_CH4.append(math.exp(-i / alpha_methane))
        fr_N2O.append(math.exp(-i / alpha_N2O))
    return fr_CO2, fr_CH4, fr_N2O


def mass_calculation(emission_CO2, emission_CO2_nonfossil, capture_CO2, emission_CH4, emission_N2O, fr_CO2, fr_CH4, fr_N2O):
    CO2_mass = []
    capture_mass = []
    CO2_nonfossil_mass = []
    CH4_mass = []
    N2O_mass = []
    x = len(emission_CO2)
    c = 0
    while c < x:
        a = c
        b = 0
        CO2_mass_calculation = 0
        capture_mass_calculation = 0
        CO2_nonfossil_mass_calculation = 0
        CH4_mass_calculation = 0
        N2O_mass_calculation = 0
        while a >= 0:
            CO2_mass_calculation = CO2_mass_calculation + (emission_CO2[a]) * fr_CO2[b]
            capture_mass_calculation = capture_mass_calculation + (capture_CO2[a]) * fr_CO2[b]
            CO2_nonfossil_mass_calculation = CO2_nonfossil_mass_calculation + (emission_CO2_nonfossil[a]) * fr_CO2[b]
            CH4_mass_calculation = CH4_mass_calculation + (emission_CH4[a]) * fr_CH4[b]
            N2O_mass_calculation = N2O_mass_calculation + (emission_N2O[a]) * fr_N2O[b]
            a = a - 1
            b = b + 1
        CO2_mass.append(CO2_mass_calculation)
        capture_mass.append(capture_mass_calculation)
        CO2_nonfossil_mass.append(CO2_nonfossil_mass_calculation)
        CH4_mass.append(CH4_mass_calculation)
        N2O_mass.append(N2O_mass_calculation)
        c = c + 1
    return CO2_mass, capture_mass, CO2_nonfossil_mass, CH4_mass, N2O_mass


def concentration_calculation(CO2_mass, capture_mass, CO2_nonfossil_mass, CH4_mass, N2O_mass):
    concentration_CO2 = []
    concentration_capture = []
    concentration_CO2_nonfossil = []
    concentration_CH4 = []
    concentration_N2O = []
    for i in range(len(CO2_mass)):
        value_CO2 = CO2_mass[i] * (1000000 / 5.15e18) / (molar_mass_CO2 / molar_mass_air)
        value_capture = capture_mass[i] * (1000000 / 5.15e18) / (molar_mass_CO2_capture / molar_mass_air)
        value_CO2_nonfossil = CO2_nonfossil_mass[i] * (1000000 / 5.15e18) / (molar_mass_CO2_nonfossil / molar_mass_air)
        value_CH4 = CH4_mass[i] * (1000000 / 5.15e18) / (molar_mass_CH4 / molar_mass_air)
        value_N2O = N2O_mass[i] * (1000000 / 5.15e18) / (molar_mass_N2O / molar_mass_air)
        concentration_CO2.append(value_CO2)
        concentration_capture.append(value_capture)
        concentration_CO2_nonfossil.append(value_CO2_nonfossil)
        concentration_CH4.append(value_CH4)
        concentration_N2O.append(value_N2O)
    return concentration_CO2, concentration_capture, concentration_CO2_nonfossil, concentration_CH4, concentration_N2O


def f(concentration_CH4, concentration_N2O):
    fMN = 0.47 * np.log(1 + 2.01e-5 * (concentration_CH4 * concentration_N2O) ** 0.75 + 5.31e-15 * concentration_CH4 * (concentration_CH4 * concentration_N2O) ** 1.52)
    return fMN


def radiative_forcing(concentration_CO2, concentration_CO2_nonfossil, concentration_capture, concentration_CH4, concentration_N2O):
    a = 0
    b = len(concentration_CO2)
    RF_CO2 = []
    RF_CH4 = []
    RF_N2O = []
    RF_capture = []
    RF_CO2_nonfossil = []
    while a < b:
        RF_CO2_additionnel = sens_RF_CO2 * np.log(1 + concentration_CO2[a] / CO2_atmospheric_concentration_2019)
        RF_capture_additionnel = sens_RF_CO2 * np.log(1 + concentration_capture[a] / CO2_atmospheric_concentration_2019)
        RF_CO2_nonfossil_additionnel = sens_RF_CO2 * np.log(1 + concentration_CO2_nonfossil[a] / CO2_atmospheric_concentration_2019)
        RF_CH4_additionnel = beta_methane * ((CH4_atmospheric_concentration_2019 + concentration_CH4[a]) ** (1 / 2) - CH4_atmospheric_concentration_2019 ** (1 / 2)) - (f(CH4_atmospheric_concentration_2019 + concentration_CH4[a], N2O_atmospheric_concentration_2019) - f(CH4_atmospheric_concentration_2019, N2O_atmospheric_concentration_2019))
        RF_N2O_additionnel = beta_N2O * ((N2O_atmospheric_concentration_2019 + concentration_N2O[a]) ** (1 / 2) - N2O_atmospheric_concentration_2019 ** (1 / 2)) - (f(CH4_atmospheric_concentration_2019, concentration_N2O[a] + N2O_atmospheric_concentration_2019) - f(CH4_atmospheric_concentration_2019, N2O_atmospheric_concentration_2019))
        RF_CO2.append(RF_CO2_additionnel)
        RF_capture.append(RF_capture_additionnel)
        RF_CO2_nonfossil.append(RF_CO2_nonfossil_additionnel)
        RF_CH4.append(RF_CH4_additionnel)
        RF_N2O.append(RF_N2O_additionnel)
        a = a + 1
    RF_total = []
    for i in range(len(RF_CO2)):
        RF_total.append(RF_CO2[i] + RF_CH4[i] + RF_N2O[i] + RF_capture[i] + RF_CO2_nonfossil[i])
    return RF_total, RF_CO2, RF_CH4, RF_N2O, RF_capture, RF_CO2_nonfossil


def climate_change(emission_CO2, emission_CO2_nonfossil, capture_CO2, emission_CH4, emission_N2O):
    fr_CO2, fr_CH4, fr_N2O = fraction_calculation()
    CO2_mass, capture_mass, CO2_nonfossil_mass, CH4_mass, N2O_mass = mass_calculation(emission_CO2, emission_CO2_nonfossil, capture_CO2, emission_CH4, emission_N2O, fr_CO2, fr_CH4, fr_N2O)
    concentration_CO2, concentration_capture, concentration_CO2_nonfossil, concentration_CH4, concentration_N2O = concentration_calculation(CO2_mass, capture_mass, CO2_nonfossil_mass, CH4_mass, N2O_mass)
    RF_total, RF_CO2, RF_CH4, RF_N2O, RF_capture, RF_CO2_nonfossil = radiative_forcing(concentration_CO2, concentration_CO2_nonfossil, concentration_capture, concentration_CH4, concentration_N2O)
    return RF_total, RF_CO2, RF_CH4, RF_N2O, RF_capture, RF_CO2_nonfossil
