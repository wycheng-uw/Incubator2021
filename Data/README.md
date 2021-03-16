# Data Summary

| Data Source | Content | URL |
| WWLLN | The World Wide Lightning Location Network operated by the University of Washington. WWLLN is a network of approximately 70 sensors that detect electromagnetic radiation (i.e., sferics) emitted by lightning strikes at very low frequency (VLF; 3.30 kHz). The propagation of sferics within the Earth. ionosphere waveguide allows for the detection of lightning at distances of thousands of kilometers, enabling WWLLN to provide global lightning detection coverage. The detection efficiency of WWLLN is approximately 10\%, with location errors less than 10 km based on comparisons with observations from the short-range lightning observation networks in North America. | http://wwlln.net/ |
| ERA5 | The fifth generation of the European Centre for Medium-Range Weather Forecasts (ECMWF) atmospheric reanalysis prodcuts. The ERA5 dataset provide the best estimate of the atmospheric variables by incorporating the best available observation data from satellites and in-situ stations with the state-of-the-art ECMWF operational forecast model. | https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5 |
| TRMM | Tropical Rainfall Measuring Mission (TRMM) Multi-satellite Precipitation Analysis dataset provides the precipitation data, which is a calibration-based sequential scheme for combining precipitation estimates from multiple satellites, as well as gauge analyses where feasible. | https://disc.gsfc.nasa.gov/datasets/TRMM_3B42_7/summary |

# Variables

| --- | --- | --- | --- | --- |
| Variable name | Full name | Dimension | Source | Descriptions |
| F | lightning stroke density (# yr-1 km-2) | Time x lat x lon | WWLLN | Number of lightning strokes per unit time/area. |
| cape | Convective available potential energy | Time x lat x lon | ERA5 | An indicator of atmospheric instability. This variable is often used to infer the intensity (convective updraft velocity) of the thunderstorm.|
| pcp | Precipitation | Time x lat x lon | TRMM | Surface precipitation |
| t | Temperature | Time x lev x lat x lon | ERA5 | |
| q | Specific humidity | Time x lev x lat x lon | ERA5 | |
| z | Geopotential height | Time x lev x lat x lon | ERA5 | |

# Data Details

- Time period: 2010/01/01 - 2019/12/31
- Time resolution: All data are gridded onto 3-hourly time resolution by taking 3-hourly average.
- Spatial resolution: All data are gridded onto 1 degree by 1 degree resolution
- Data domain: 20N - 60N, 135W - 60W
- Target domain: 32N - 42N, 120W - 110W

