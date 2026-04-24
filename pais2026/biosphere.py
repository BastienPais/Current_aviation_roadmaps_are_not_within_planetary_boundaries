from .utils import multiply_list

MSA_factor = 6.31342e12  # % loss m² °C-1 Source: Hanafiah et al. (2012)
total_area = 1.3e14  # total area of the natural and non-natural biomes in the IMAGE model Source: Alkemade et al. (2009)
climate_sens_param = 1.06  # climate sensitivity parameter Source: IPCC AR5 and Ryberg et al. (2018)
CF_BII_climate = 100 * (MSA_factor * climate_sens_param) / total_area


def biosphere_integrity(RF):
    BII = multiply_list(RF, CF_BII_climate)
    return BII
