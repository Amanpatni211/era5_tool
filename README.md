# ERA5 Downloader Tool

A simple and efficient tool for downloading ERA5 reanalysis data from the Analysis-Ready, Cloud-Optimized (ARCO) ERA5 dataset. This tool is designed for researchers who need quick access to ERA5 data with flexible options for spatial and temporal selection.

## Features

- Download pressure level variables at selected pressure levels
- Download single-level/surface variables
- Apply spatial subsetting (select a specific geographical region)
- Apply temporal selection (specific date)
- Visualize downloaded data with automatic plotting
- Analysis-ready data access via Google Cloud Storage

## Quick Start

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Amanpatni211/era5_tool.git
   cd era5_tool
   ```

2. Set up the environment:
   ```bash
   ./setup.sh
   ```
   This will create a Python virtual environment and install all required dependencies.

3. Activate the environment:
   ```bash
   source era5_env/bin/activate
   ```

### Basic Usage

Download temperature at 850 hPa for a specific date:
```bash
python era5_download.py --year 2023 --month 1 --day 1 --variables temperature --levels 850
```

Download data for a specific region (e.g., Europe):
```bash
python era5_download.py --year 2023 --month 1 --day 1 --variables temperature --levels 850 \
  --lat_min 35 --lat_max 60 --lon_min -10 --lon_max 30 \
  --output_dir ./my_data
```

Visualize downloaded data:
```bash
python era5_visualize.py ./my_data/temperature_850_20230101.nc
```

## Documentation

For complete documentation and examples, see the [User Guide](./docs/user_guide.md).

## Available Variables

See the [Variables List](./docs/variables.md) for a complete list of available variables.

## Requirements

- Python 3.8+
- Required packages (automatically installed by setup.sh):
  - xarray
  - zarr
  - fsspec
  - gcsfs
  - dask
  - netCDF4
  - matplotlib
  - numpy
  - pandas

## References

This tool accesses ERA5 data from the [ARCO-ERA5](https://github.com/google-research/arco-era5) project, which provides Analysis-Ready, Cloud-Optimized ERA5 data hosted on Google Cloud Storage.
