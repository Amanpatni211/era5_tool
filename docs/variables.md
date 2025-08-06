# ERA5 Available Variables

This document lists the commonly used ERA5 variables available through the ERA5 Downloader Tool.

## Pressure Level Variables

These variables are available at multiple pressure levels (37 levels from 1 to 1000 hPa):

| Variable | Name in ECMWF | Description | Unit |
|----------|---------------|-------------|------|
| geopotential | z | Geopotential height | m²/s² |
| specific_humidity | q | Specific humidity | kg/kg |
| temperature | t | Air temperature | K |
| u_component_of_wind | u | Eastward wind component | m/s |
| v_component_of_wind | v | Northward wind component | m/s |
| fraction_of_cloud_cover | cc | Cloud cover fraction | (0-1) |
| ozone_mass_mixing_ratio | o3 | Ozone concentration | kg/kg |
| specific_cloud_ice_water_content | ciwc | Ice content in clouds | kg/kg |
| specific_cloud_liquid_water_content | clwc | Liquid water content in clouds | kg/kg |
| potential_vorticity | pv | Potential vorticity | K m²/kg/s |
| vertical_velocity | w | Vertical velocity (omega) | Pa/s |

## Surface/Single Level Variables

These variables are available at single levels (typically the surface or specific heights):

| Variable | Name in ECMWF | Description | Unit |
|----------|---------------|-------------|------|
| 2m_temperature | 2t | Temperature at 2m above surface | K |
| 2m_dewpoint_temperature | 2d | Dewpoint temperature at 2m | K |
| 10m_u_component_of_wind | 10u | Eastward wind at 10m | m/s |
| 10m_v_component_of_wind | 10v | Northward wind at 10m | m/s |
| mean_sea_level_pressure | msl | Sea level pressure | Pa |
| surface_pressure | sp | Surface pressure | Pa |
| total_precipitation | tp | Total precipitation | m |
| total_cloud_cover | tcc | Total cloud cover | (0-1) |
| sea_surface_temperature | sst | Sea surface temperature | K |

## Pressure Levels

The ERA5 dataset provides data at 37 pressure levels (in hPa):

1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000

## Additional Variables

Many more variables are available in the ERA5 dataset. The downloader will display a list of available variables if you request one that's not found. You can also check the [ECMWF parameter database](https://codes.ecmwf.int/grib/param-db) for a complete list.