#!/usr/bin/env python3
"""
ERA5 Downloader with Unique Filenames

This is a modified version of the original era5_download.py that ensures unique filenames
by adding a timestamp to prevent overwriting existing files.
"""

import os
import sys
import time
import argparse
import numpy as np
from datetime import datetime
from pathlib import Path

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

# Check if required packages are available
try:
    import xarray as xr
    import fsspec
    import zarr
    print("✓ Required packages loaded successfully")
except ImportError as e:
    print(f"Error: Required package not found - {e}")
    print("Please run setup.sh to install all required dependencies")
    sys.exit(1)

# ARCO ERA5 path for analysis-ready data
GCP_AR_DIRECTORY = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"

# Available ERA5 variables lists
PRESSURE_LEVEL_VARIABLES = [
    "geopotential", "specific_humidity", "temperature", "u_component_of_wind", 
    "v_component_of_wind", "fraction_of_cloud_cover", "ozone_mass_mixing_ratio",
    "specific_cloud_ice_water_content", "specific_cloud_liquid_water_content",
    "potential_vorticity", "vertical_velocity"
]

SURFACE_VARIABLES = [
    "2m_temperature", "2m_dewpoint_temperature", "10m_u_component_of_wind",
    "10m_v_component_of_wind", "mean_sea_level_pressure", "surface_pressure",
    "total_precipitation", "total_cloud_cover", "sea_surface_temperature"
]

# All available pressure levels in ERA5
PRESSURE_LEVELS = [1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 125, 150, 175, 200, 225,
                   250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 775, 800,
                   825, 850, 875, 900, 925, 950, 975, 1000]

def download_era5_data(year, month, day, variables=None, pressure_levels=None, 
                      lat_range=None, lon_range=None, output_dir="./data"):
    """
    Download ERA5 data from the Analysis-Ready dataset.
    
    Args:
        year (int): Year of the data
        month (int): Month of the data
        day (int): Day of the data
        variables (list): List of variables to download (None = all available)
        pressure_levels (list): List of pressure levels (None = all available)
        lat_range (tuple): (min_lat, max_lat) or None for global
        lon_range (tuple): (min_lon, max_lon) or None for global
        output_dir (str): Directory to save data
    """
    print(f"Downloading ERA5 data for {year}-{month:02d}-{day:02d}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Step 1: Open the zarr dataset
    print("\nStep 1: Opening ARCO ERA5 dataset...")
    try:
        start_time = time.time()
        ds = xr.open_zarr(
            GCP_AR_DIRECTORY,
            chunks=None,  # Let xarray/dask handle chunking
            storage_options=dict(token='anon'),
        )
        elapsed = time.time() - start_time
        print(f"✓ Successfully opened dataset in {elapsed:.2f} seconds")
        print(f"Dataset shape: {ds.dims}")
        print(f"Time range: {ds.time.min().values} to {ds.time.max().values}")
    except Exception as e:
        print(f"Error opening dataset: {str(e)}")
        return
    
    # Step 2: Select date
    print("\nStep 2: Selecting date...")
    try:
        start_time = time.time()
        date_str = f"{year}-{month:02d}-{day:02d}"
        ds_day = ds.sel(time=date_str)
        elapsed = time.time() - start_time
        print(f"✓ Successfully selected date {date_str} in {elapsed:.2f} seconds")
    except Exception as e:
        print(f"Error selecting date: {str(e)}")
        return
    
    # Step 3: Filter variables if specified
    print("\nStep 3: Filtering variables...")
    if variables is not None:
        try:
            start_time = time.time()
            # Find which requested variables are available
            available_vars = [var for var in variables if var in ds_day.variables]
            if not available_vars:
                print("  None of the requested variables found in dataset")
                print(f"  Available variables: {list(ds_day.data_vars)[:10]}...")
                # Use first few variables as a fallback
                available_vars = list(ds_day.data_vars)[:3]
            
            ds_day = ds_day[available_vars]
            elapsed = time.time() - start_time
            print(f"✓ Selected variables: {available_vars} in {elapsed:.2f} seconds")
        except Exception as e:
            print(f"Error filtering variables: {str(e)}")
    else:
        # Limit to a few variables for testing
        available_vars = list(ds_day.data_vars)[:3]
        ds_day = ds_day[available_vars]
        print(f"  Using default variables: {available_vars}")
    
    # Step 4: Filter pressure levels if specified
    print("\nStep 4: Filtering pressure levels...")
    if 'level' in ds_day.dims and pressure_levels is not None:
        try:
            start_time = time.time()
            # Convert all pressure levels to integers for comparison
            available_levels = ds_day.level.values
            requested_levels = [int(lvl) for lvl in pressure_levels]
            
            # Find which levels are available
            levels_to_use = [lvl for lvl in requested_levels if lvl in available_levels]
            
            if levels_to_use:
                ds_day = ds_day.sel(level=levels_to_use)
                elapsed = time.time() - start_time
                print(f"✓ Selected pressure levels: {levels_to_use} in {elapsed:.2f} seconds")
            else:
                print("  None of the requested pressure levels found")
                print(f"  Available levels: {available_levels}")
        except Exception as e:
            print(f"Error filtering pressure levels: {str(e)}")
    elif 'level' in ds_day.dims:
        # Use just a few pressure levels for testing
        available_levels = ds_day.level.values
        levels_to_use = [500, 850] if 500 in available_levels and 850 in available_levels else available_levels[:2]
        ds_day = ds_day.sel(level=levels_to_use)
        print(f"  Using default pressure levels: {levels_to_use}")
    else:
        print("  No pressure levels dimension found in dataset")
    
    # Step 5: Apply spatial subsetting (latitude only first)
    print("\nStep 5: Applying spatial subsetting...")
    if lat_range is not None:
        try:
            start_time = time.time()
            min_lat, max_lat = lat_range
            
            # ERA5 latitudes go from 90° to -90° (north to south)
            # Make sure min_lat < max_lat
            if min_lat > max_lat:
                min_lat, max_lat = max_lat, min_lat
                
            # Find actual latitude values that exist in the dataset
            # This is crucial because xarray.sel() with "nearest" method can be more reliable
            closest_min_lat = float(ds_day.latitude.sel(latitude=min_lat, method="nearest").values)
            closest_max_lat = float(ds_day.latitude.sel(latitude=max_lat, method="nearest").values)
            
            print(f"  Requested latitude range: {min_lat} to {max_lat}")
            print(f"  Actual latitude range used: {closest_min_lat} to {closest_max_lat}")
            
            # Apply latitude subset with nearest method
            ds_day = ds_day.sel(latitude=slice(closest_max_lat, closest_min_lat))
            
            elapsed = time.time() - start_time
            print(f"✓ Successfully applied latitude subsetting in {elapsed:.2f} seconds")
            print(f"  Resulting dimensions: {ds_day.dims}")
        except Exception as e:
            print(f"Error applying latitude subsetting: {str(e)}")
    
    # Step 6: Apply longitude subsetting
    if lon_range is not None:
        try:
            start_time = time.time()
            min_lon, max_lon = lon_range
            
            # ERA5 longitudes go from 0° to 359.75° (west to east)
            # Make sure min_lon < max_lon
            if min_lon > max_lon:
                min_lon, max_lon = max_lon, min_lon
                
            # Find actual longitude values that exist in the dataset
            closest_min_lon = float(ds_day.longitude.sel(longitude=min_lon, method="nearest").values)
            closest_max_lon = float(ds_day.longitude.sel(longitude=max_lon, method="nearest").values)
            
            print(f"  Requested longitude range: {min_lon} to {max_lon}")
            print(f"  Actual longitude range used: {closest_min_lon} to {closest_max_lon}")
            
            # Apply longitude subset with nearest method
            ds_day = ds_day.sel(longitude=slice(closest_min_lon, closest_max_lon))
            
            elapsed = time.time() - start_time
            print(f"✓ Successfully applied longitude subsetting in {elapsed:.2f} seconds")
            print(f"  Resulting dimensions: {ds_day.dims}")
        except Exception as e:
            print(f"Error applying longitude subsetting: {str(e)}")
    
    # Step 7: Save the data
    print("\nStep 6: Saving data...")
    saved_count = 0
    total_size_mb = 0
    
    for var_name in ds_day.data_vars:
        try:
            var_data = ds_day[var_name]
            
            # Check if this is a multi-level or single-level variable
            is_multilevel = 'level' in var_data.dims
            
            if is_multilevel:
                for level in var_data.level.values:
                    level_data = var_data.sel(level=level)
                    
                    # Create a unique filename with timestamp
                    filename = f"{var_name}_{int(level)}_{year}{month:02d}{day:02d}_{timestamp}.nc"
                    output_file = os.path.join(output_dir, filename)
                    
                    # Save to NetCDF with compression
                    encoding = {var_name: {'zlib': True, 'complevel': 5}}
                    level_data.to_netcdf(output_file, encoding=encoding)
                    
                    # Calculate size
                    file_size = os.path.getsize(output_file) / (1024 * 1024)
                    total_size_mb += file_size
                    saved_count += 1
                    
                    print(f"  Saved {filename}: {file_size:.2f} MB")
            else:
                # Create a unique filename with timestamp
                filename = f"{var_name}_sfc_{year}{month:02d}{day:02d}_{timestamp}.nc"
                output_file = os.path.join(output_dir, filename)
                
                # Save to NetCDF with compression
                encoding = {var_name: {'zlib': True, 'complevel': 5}}
                var_data.to_netcdf(output_file, encoding=encoding)
                
                # Calculate size
                file_size = os.path.getsize(output_file) / (1024 * 1024)
                total_size_mb += file_size
                saved_count += 1
                
                print(f"  Saved {filename}: {file_size:.2f} MB")
                
        except Exception as e:
            print(f"  Error saving {var_name}: {str(e)}")
    
    print(f"\n✓ Summary: Saved {saved_count} files ({total_size_mb:.2f} MB) to {output_dir}")
    return saved_count

def main():
    parser = argparse.ArgumentParser(description="Download ERA5 data with unique filenames")
    parser.add_argument("--year", type=int, required=True, help="Year of the data (e.g., 2023)")
    parser.add_argument("--month", type=int, required=True, help="Month of the data (1-12)")
    parser.add_argument("--day", type=int, required=True, help="Day of the data (1-31)")
    parser.add_argument("--variables", type=str, nargs="+", help="Specific variables to download")
    parser.add_argument("--levels", type=int, nargs="+", help="Specific pressure levels to download")
    parser.add_argument("--lat_min", type=float, help="Minimum latitude")
    parser.add_argument("--lat_max", type=float, help="Maximum latitude")
    parser.add_argument("--lon_min", type=float, help="Minimum longitude")
    parser.add_argument("--lon_max", type=float, help="Maximum longitude")
    parser.add_argument("--output_dir", type=str, default="./data", help="Directory to save the downloaded data")
    
    args = parser.parse_args()
    
    # Process lat/lon range arguments
    lat_range = None
    if args.lat_min is not None and args.lat_max is not None:
        lat_range = (args.lat_min, args.lat_max)
    
    lon_range = None
    if args.lon_min is not None and args.lon_max is not None:
        lon_range = (args.lon_min, args.lon_max)
    
    # Download the data
    download_era5_data(
        args.year, args.month, args.day,
        variables=args.variables,
        pressure_levels=args.levels,
        lat_range=lat_range,
        lon_range=lon_range,
        output_dir=args.output_dir
    )

if __name__ == "__main__":
    main()