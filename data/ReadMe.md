This repository provides a reproducible framework to assess the absolute environmental sustainability of global aviation transition scenarios using prospective Life Cycle Assessment (LCA) aligned with the planetary boundaries framework.

📄 **Preprint**: https://doi.org/10.21203/rs.3.rs-5409598/v1

📦 **Data & code archive**: [![DOI][(https://zenodo.org/badge/791878165.svg)](https://doi.org/10.5281/zenodo.19739876)](https://doi.org/10.5281/zenodo.14186426)

🌍 **Overview**

This framework allows you to:

- Build aviation transition scenarios
- Model energy demand trajectories (1940–2050)
- Compute life cycle environmental impacts
- Perform Absolute Environmental Sustainability Assessment (AESA)
- Explore sensitivities (traffic growth, IAMs, etc.)
- Generate publication-ready figures

📂 **Repository structure**


├── data/                  
├── pais2026/
│   ├── _init_.py       
│   ├── aesa.py         
│   ├── biosphere.py            
│   ├── climate.py 
│   ├── config.py       
│   ├── downscaling.py         
│   ├── historical.py            
│   ├── impacts.py 
│   ├── main.py       
│   ├── resources.py         
│   ├── scenarios.py            
│   ├── utils.py 
│   ├── PAIS_2026_Code.ipynb
└── README.md


📊 **Outputs**

The framework produces:


- Fuel mix evolution (2023–2050)
- AESA indicators across planetary boundaries:
  - Climate change (RF)
  - Biosphere integrity (%BII)
  - Nitrogen (Tg N yr-1)
  - Phosphorus (Tg P yr-1)
  - Freshwater use (km3)
  - Stratospheric ozone depletion (DU)
- Resource use:
  - Biomass demand (EJ)
  - Electricity demand (EJ)
  - Land occupation (mega-km2)
  - Water withdrawal (km3)
  - Direct air capture (MtCO2)
 
🔗 **Related tools**

This work builds upon the *premise* framework for prospective LCA.

💻 GitHub repository: https://github.com/polca/premise

📄 Scientific article: [https://doi.org/10.1016/j.jclepro.2021.127125](https://doi.org/10.1016/j.rser.2022.112311)
