#!/usr/bin/env python3
"""
ERA5 Data Visualization Tool

This script provides visualization capabilities for ERA5 NetCDF files.
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

# Check if required packages are available
try:
    import xarray as xr
    print("✓ Required packages loaded successfully")
except ImportError as e:
    print(f"Error: Required package not found - {e}")
    print("Please run setup.sh to install all required dependencies")
    sys.exit(1)

def plot_era5_file(filepath, output_dir="./plots"):
    """Plot an ERA5 NetCDF file with proper metadata"""
    try:
        # Load the NetCDF file
        print(f"Loading {filepath}...")
        ds = xr.open_dataset(filepath)
        
        # Get the variable name (first data variable)
        var_name = list(ds.data_vars)[0]
        data = ds[var_name]
        
        # Get metadata
        filename = Path(filepath).name
        level = "surface"
        if "_sfc_" not in filename and "_" in filename:
            level_parts = filename.split("_")
            if len(level_parts) > 1 and level_parts[1].isdigit():
                level = f"{level_parts[1]} hPa"
                
        date_str = ""
        if filename[-11:-3].isdigit():
            date_str = filename[-11:-3]
            date_str = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            
        # Create figure for map
        plt.figure(figsize=(12, 8))
        
        # Create appropriate colormap based on variable
        cmap = 'viridis'
        if 'temperature' in var_name:
            cmap = 'RdBu_r'
        elif 'geopotential' in var_name:
            cmap = 'terrain'
        elif 'pressure' in var_name:
            cmap = 'rainbow'
        elif any(term in var_name for term in ['precipitation', 'rain', 'snow']):
            cmap = 'Blues'
        elif any(term in var_name for term in ['wind', 'u_component', 'v_component']):
            cmap = 'coolwarm'
        
        # For multiple timesteps, plot the first timestep
        if 'time' in data.dims and data.time.size > 1:
            print(f"Multiple timesteps found ({data.time.size}), plotting the first one")
            plot_data = data.isel(time=0)
            time_str = str(data.time.values[0])[:16].replace('T', ' ')
        else:
            plot_data = data
            time_str = ""
            
        # Create the plot
        img = plot_data.plot(cmap=cmap)
        
        # Set title and labels
        var_title = var_name.replace('_', ' ').title()
        title = f"{var_title} at {level}"
        if date_str:
            title += f" - {date_str}"
        if time_str:
            title += f" {time_str}"
            
        plt.title(title, fontsize=14)
        plt.xlabel("Longitude", fontsize=12)
        plt.ylabel("Latitude", fontsize=12)
        
        # Add colorbar label with units
        units = getattr(data, 'units', '')
        if not units:
            if 'temperature' in var_name:
                units = 'K'
            elif 'geopotential' in var_name:
                units = 'm²/s²'
            elif 'pressure' in var_name:
                units = 'Pa'
        
        if img.colorbar:
            img.colorbar.set_label(units)
            
        # Create output directory if it doesn't exist
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save the plot
        output_file = output_dir / f"{Path(filepath).stem}.png"
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        print(f"Plot saved to {output_file}")
        
        # Show statistics
        print(f"\nStatistics for {var_name}:")
        print(f"  Dimensions: {data.dims}")
        print(f"  Shape: {data.shape}")
        print(f"  Min: {float(data.min().values):.2f}")
        print(f"  Max: {float(data.max().values):.2f}")
        print(f"  Mean: {float(data.mean().values):.2f}")
        
        # Time information
        if 'time' in data.dims and data.time.size > 0:
            print(f"  Time range: {str(data.time.min().values)[:19]} to {str(data.time.max().values)[:19]}")
        
        # Spatial information
        if 'latitude' in data.dims and 'longitude' in data.dims:
            print(f"  Latitude range: {float(data.latitude.min().values):.2f}° to {float(data.latitude.max().values):.2f}°")
            print(f"  Longitude range: {float(data.longitude.min().values):.2f}° to {float(data.longitude.max().values):.2f}°")
            
        # Check if we're plotting a time series
        if 'time' in data.dims and data.time.size > 1:
            print("\nWould you like to see a time series plot? (y/n)")
            choice = input().strip().lower()
            if choice == 'y':
                plot_time_series(data, var_name, level, output_dir)
        
    except Exception as e:
        print(f"Error plotting {filepath}: {e}")
        import traceback
        traceback.print_exc()

def plot_time_series(data, var_name, level, output_dir):
    """Generate time series plots for the data"""
    try:
        # Create a new figure for the time series
        plt.figure(figsize=(14, 6))
        
        # If the data has latitude and longitude, average them to get a time series
        if 'latitude' in data.dims and 'longitude' in data.dims:
            ts_data = data.mean(dim=['latitude', 'longitude'])
            plt.plot(ts_data.time, ts_data.values, 'b-', linewidth=2)
            plt.title(f"Time Series of {var_name.replace('_', ' ').title()} at {level} (Spatial Mean)", fontsize=14)
        else:
            # Otherwise plot the time series directly
            plt.plot(data.time, data.values, 'b-', linewidth=2)
            plt.title(f"Time Series of {var_name.replace('_', ' ').title()} at {level}", fontsize=14)
        
        plt.grid(True)
        plt.xlabel('Time', fontsize=12)
        
        # Add units to y-axis
        units = getattr(data, 'units', '')
        if not units:
            if 'temperature' in var_name:
                units = 'K'
            elif 'geopotential' in var_name:
                units = 'm²/s²'
            elif 'pressure' in var_name:
                units = 'Pa'
        plt.ylabel(f"{var_name.replace('_', ' ').title()} ({units})", fontsize=12)
        
        # Save the plot
        output_file = Path(output_dir) / f"{var_name}_time_series.png"
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        print(f"Time series plot saved to {output_file}")
        
    except Exception as e:
        print(f"Error creating time series plot: {e}")

def main():
    """Main function to process command-line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python era5_visualize.py <path_to_netcdf_file> [output_directory]")
        sys.exit(1)
        
    filepath = sys.argv[1]
    output_dir = "./plots"
    
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    plot_era5_file(filepath, output_dir)

if __name__ == "__main__":
    main()