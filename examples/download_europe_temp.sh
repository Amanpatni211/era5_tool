#!/bin/bash
#
# Example: Download temperature data for Europe
#
# This script demonstrates how to download temperature data for Europe
# at the 850 hPa pressure level for January 1, 2023.
#

# Navigate to the tool directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# Activate the environment
source era5_env/bin/activate

# Create output directory
OUTPUT_DIR="./data/europe"
mkdir -p $OUTPUT_DIR

# Download temperature data for Europe
python scripts/era5_download.py \
  --year 2023 \
  --month 1 \
  --day 1 \
  --variables temperature \
  --levels 850 \
  --lat_min 35 \
  --lat_max 60 \
  --lon_min -10 \
  --lon_max 30 \
  --output_dir $OUTPUT_DIR

# Visualize the downloaded data
if [ -f "$OUTPUT_DIR/temperature_850_20230101.nc" ]; then
    python scripts/era5_visualize.py "$OUTPUT_DIR/temperature_850_20230101.nc" "./plots"
else
    echo "Download failed, no file to visualize"
fi

# Deactivate the environment
deactivate