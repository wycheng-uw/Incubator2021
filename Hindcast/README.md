# Hindcast analysis

## Goal
The goal of this subproject is to test the predictability of lightning flash rate (F) in the forecast model. 
In TK18, the baseline predictability of F is tested using the GEFS Hindcast dataset with R14 lightning parameterization scheme, which shows that the forecast skill is significant up to 15 days in forecast lead time. 
Our goal is to test if the ML-based F parameterization schemes can outperform the R14 method and achieve a greater forecast skill and/or with longer lead time.

## Scripts:
- TK18.ipynb: Used to reproduce the results in TK18, except that using WWLLN data instead of NLDN.
- GEFS_2d_variables_download.py: Used to download the GEFS hindcast dataset.

## Data Source:
- GEFS: http://iridl.ldeo.columbia.edu/SOURCES/.Models/.SubX/.EMC/.GEFS/.hindcast/

## Reference
- D. M. Romps, J. T. Seeley, D. Vollaro, J. Molinari (2014), Science (80-. ). 346, 851-854.
- M. K. Tippett, W. J. Koshak (2018), Geophys. Res. Lett., doi:10.1029/2018GL079750.

