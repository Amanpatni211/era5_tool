#!/bin/bash
#
# Example: Download surface variables
#
# This script demonstrates how to download surface variables (mean sea level pressure
# and 2m temperature) for January 1, 2023.
#

# Navigate to the tool directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# Activate the environment
source era5_env/bin/activate

# Create output directory
OUTPUT_DIR="./data/surface"
mkdir -p $OUTPUT_DIR

# Download surface variables
python scripts/era5_download.py \
  --year 2023 \
  --month 1 \
  --day 1 \
  --variables mean_sea_level_pressure 2m_temperature \
  --output_dir $OUTPUT_DIR

# Visualize the downloaded data
if [ -f "$OUTPUT_DIR/mean_sea_level_pressure_sfc_20230101.nc" ]; then
    python scripts/era5_visualize.py "$OUTPUT_DIR/mean_sea_level_pressure_sfc_20230101.nc" "./plots"
fi

if [ -f "$OUTPUT_DIR/2m_temperature_sfc_20230101.nc" ]; then
    python scripts/era5_visualize.py "$OUTPUT_DIR/2m_temperature_sfc_20230101.nc" "./plots"
fi

# Deactivate the environment
deactivate