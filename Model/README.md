# ML analysis

## Goal
The goal of this subproject is to test the predictability of lightning flash rate (F) using observed atmospheric state variables as input. 
Various input variables are explored to test if they can provide useful information in predicting F, including vertical profiles of temperature, moisture, and 2D images of geopotential height. The performance of the ML models is tested against an empirically based lightning parameterization scheme proposed by Romps et al. (2014). Our goal is to test if the ML-based F parameterization schemes can outperform the R14 method.

## Scripts:
- main.ipynb: Used to test the different configurations of ML settings and their performance in predicting F.

## Data Source:
- WWLLN: http://wwlln.net/

## Reference
- D. M. Romps, J. T. Seeley, D. Vollaro, J. Molinari (2014), Science (80-. ). 346, 851-854.

