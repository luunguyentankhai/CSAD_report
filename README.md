# The Impact of COVID-19 Pandemic on Investor Herding Behavior: Evidence from the Vietnamese Stock Market

# SETUP

#### Remember you are in project folder

- Using a python version 3.11

- Create a venv use this command in you terminal

 `python -m venv venv`

- Enter into venv 

**For Windows**
 `venv/Scripts/activate`

**For Linux/MacOS**
 `source venv/bin/activate`

- Run a pip install to install lib and collect the data

 `pip install -r requirements.txt`

# FOLDER STRUCTURE
 ```
    .
├── config.py
├── data
│   ├── processed
│   └── raw
│       ├── Data.csv
│       ├── agriculture_forestry_rubber
│       ├── banking
│       ├── chemicals_fertilizers_plastics
│       ├── construction_installation
│       ├── construction_materials_mining
│       ├── food_beverage
│       ├── infrastructure_industrial_parks
│       ├── oil_gas_energy_power
│       ├── pharmaceuticals_healthcare_insurance
│       ├── real_estate
│       ├── retail_commerce
│       ├── securities_financial_services
│       ├── technology_telecommunications_multi_industry
│       ├── textiles_wood_consumer_goods
│       └── transportation_seaports_aviation
├── main.py
├── README.md
├── requirements.txt
└── scripts
    ├── Collectdata.py
    ├── __init__.py
    ├── Models
    │   ├── CSAD.py
    │   ├── Des_Sta.py
    │   ├── __init__.py
    │   ├── Multicolliner_check.py
    │   └── OLS.py
    └── Processed.py

21 directories, 13 files
 ```
# Algorithm & Methodology

### Cross-Sectional Absolute Deviation

$$
    CSAD_t = \frac{1}{N} \sum_{i=1}^{N} |R_{i,t} - R_{m,t}|
$$

### Base OLS Regression

$$
    CSAD_t = \alpha + \gamma_1 |R_{m,t}| + \gamma_2 R_{m,t}^2 + \epsilon_t
$$

### Orthogonalization

Quadratic models inherently suffer from **Structural Multicollinerity** between $|R_{m,t}|$ and $R_{m,t}^2$, which severely inflates the Variance Inflation Factor (VIF). To address this, an orthogonalization process is applied:

1. Regress $|R_{m,t}|$ on $R_{m,t}^2$
2. Extract the Residuals from this auxiliary regression
3. Replace the raw $R_{m,t}^2$ variable with these pure residuals in the main model

This technique strictly reduces the VIF to an ideal level($\approx 1.0$), ensuring highly reliable standard errors and p-values without altering the underlying economic intuition.

### Sub-sample Analysis

- Pre-Covid (H1) : 01/01/2019 - 31/01/2020
- In-Covid (H2) : 01/02/2020 - 31/03/2022
- Post-Covid (H3) : 01/04/2022 - 01/01/2024

# Code Execution & Variable Mapping

### Important Variable

- **CSAD_t**: The Cross-Sectional Absolute Deviation of returns (Dependent variable).
- **Abs_R_m_t**: The absolute cross-sectional market return ($|R_{m,t}|$). This acts as the linear base variable.
- **R_m_t^2**: The squared market return ($R_{m,t}^2$).
    
    ⚠️ ***Crucial Developer Note***: In the final dataset, this is NOT the raw squared value. The script automatically replaces this column with its orthogonalized residuals (derived from regressing against Abs_R_m_t) to eliminate structural multicollinearity before feeding it into the OLS model.

- **H1, H2, H3**: Internal boolean masks used exclusively by the script to slice the master dataset into the Pre-Covid, In-Covid, and Post-Covid sub-samples.

### Data Pipeline Flow

The automated execution pipeline consists of 4 core steps:
1. **Data Fetching**: Reads the target list from `Data.csv`. Automatically fetches historical trading data and organizes it into the `data/raw/<Sector>/{ticker}.csv` directory structure.

2. **Preprocessing & Aggregation**: Cleans the data (drops `NA` rows to prevent matrix offset errors), calculates daily log returns, and groups by date to extract the market return ($R_{m,t}$) and the dispersion index ($CSAD_t$).

3. **Sub-sample Orthogonalization**: Slices the dataset into the three defined periods. The orthogonalization algorithm is executed independently within each period to strictly force the VIF to an optimal level ($\approx 1.0$).

4. **Regression & Reporting**: Fits the OLS regression model for each period. Outputs are printed directly to the terminal and exported as validation files.

### Expected Outputs

Upon completion, the system returns a comprehensive result set for each independent period via two methods:

- **Console Output**: Prints the Correlation Matrix, VIF scores, and the OLS Regression Summary directly to the terminal. The analytical focus should be on the `coef` and `P>|t|` of the `R_m_t^2` variable.

- **Automated File Saving**: Automatically exports and saves all diagnostic matrices and regression tables as `.csv` files in the root directory.
