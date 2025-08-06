# ERA5 Downloader Tool - User Guide

This guide provides detailed instructions on using the ERA5 Downloader Tool for researchers who need to access ERA5 reanalysis data.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Command Line Options](#command-line-options)
- [Examples](#examples)
- [Visualizing Data](#visualizing-data)
- [Data Storage](#data-storage)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.8+
- Git (for cloning the repository)

### Step-by-Step Installation

1. Clone the repository:
   ```bash
   git clone https://your-repository-url/era5_tool.git
   cd era5_tool
   ```

2. Set up the environment:
   ```bash
   ./setup.sh
   ```
   This script will:
   - Create a Python virtual environment named `era5_env`
   - Install all required dependencies
   - Make the scripts executable

3. Activate the environment:
   ```bash
   source era5_env/bin/activate
   ```

## Basic Usage

The main script for downloading ERA5 data is `era5_download.py`. Here's the basic usage:

```bash
python era5_download.py --year YYYY --month MM --day DD [options]
```

## Command Line Options

### Required Parameters

- `--year`: Year of data to download (e.g., 2023)
- `--month`: Month of data (1-12)
- `--day`: Day of data (1-31)

### Optional Parameters

#### Variable Selection
- `--variables`: List of specific variables to download (space-separated)
  Example: `--variables temperature specific_humidity`

#### Level Selection
- `--levels`: List of specific pressure levels to download (space-separated)
  Example: `--levels 500 850`

#### Spatial Domain Selection
- `--lat_min`: Minimum latitude
- `--lat_max`: Maximum latitude
- `--lon_min`: Minimum longitude
- `--lon_max`: Maximum longitude

#### Output Options
- `--output_dir`: Directory to save downloaded files (default: ./data)

## Examples

### Downloading a Single Variable

Download temperature at 850 hPa for January 1, 2023:
```bash
python era5_download.py --year 2023 --month 1 --day 1 --variables temperature --levels 850
```

### Downloading Multiple Variables and Levels

Download temperature and geopotential at 500 hPa and 850 hPa:
```bash
python era5_download.py --year 2023 --month 1 --day 1 --variables temperature geopotential --levels 500 850
```

### Downloading Data for a Specific Region

Download temperature for Europe:
```bash
python era5_download.py --year 2023 --month 1 --day 1 \
  --variables temperature --levels 850 \
  --lat_min 35 --lat_max 60 --lon_min -10 --lon_max 30 \
  --output_dir ./europe_data
```

### Downloading Surface Variables

Download mean sea level pressure and 2m temperature:
```bash
python era5_download.py --year 2023 --month 1 --day 1 \
  --variables mean_sea_level_pressure 2m_temperature \
  --output_dir ./surface_data
```

## Visualizing Data

Use the `era5_visualize.py` script to visualize downloaded data:

```bash
python era5_visualize.py path/to/file.nc
```

This will:
1. Generate a plot of the data
2. Save the plot to the `./plots` directory
3. Display statistics about the data (min, max, mean, dimensions)

## Data Storage

### File Naming Convention

Files are named according to the following pattern:
- For pressure level variables: `{variable}_{level}_{YYYYMMDD}.nc`
  Example: `temperature_850_20230101.nc`
- For surface variables: `{variable}_sfc_{YYYYMMDD}.nc`
  Example: `mean_sea_level_pressure_sfc_20230101.nc`

### File Format

All data is saved in NetCDF4 format with compression. These files can be easily processed with:
- Python: xarray, netCDF4
- MATLAB: nctoolbox
- R: ncdf4
- CDO (Climate Data Operators)

## Troubleshooting

### Common Issues

1. **Package not found errors**:
   - Make sure you've activated the environment: `source era5_env/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **Connection errors when downloading**:
   - Check your internet connection
   - Google Cloud Storage may have temporary issues - try again later

3. **Memory errors with large downloads**:
   - Reduce the spatial domain using the lat/lon parameters
   - Download fewer variables or pressure levels at once
   - Increase available memory or use a machine with more RAM

4. **Variable not found errors**:
   - Check the spelling of the variable name
   - See the [variables list](./variables.md) for available variables

For additional help, please contact the repository maintainers.