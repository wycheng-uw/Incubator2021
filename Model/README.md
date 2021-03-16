# ML analysis

- Use plot_overview.ipynb to generate visuals to investigate the weather patterns for any given time.

## Step 1.
- run_CreateDataset.ipynb
- Integrate the dataset and save them in the netCDF format

## Step 2.
- run_ClassifierSensitivityTest.ipynb
- Test the performance of each ML classifier in terms of AUCROC and AUCPRC scores

## Step 3.
- run_FeatureSensitivityTest.ipynb
- Varying the input feature to optimize the ML classifier's performance 

## Step 4.
- run_RegressorSensitivityTest.ipynb
- Test the performance of each ML regressor, which are then compared with an physical lightning parameterization methods (Romps et al., 2014)

## Reference
- D. M. Romps, J. T. Seeley, D. Vollaro, J. Molinari (2014), Science (80-. ). 346, 851-854.

