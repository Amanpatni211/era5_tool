#!/bin/bash
#
# ERA5 Tool Setup Script
#
# This script creates a Python environment and installs all required dependencies.
#

# Determine the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_NAME="era5_env"
ENV_DIR="$SCRIPT_DIR/$ENV_NAME"

echo "=== ERA5 Tool Setup ==="
echo "Setting up environment in: $ENV_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Create a requirements.txt file
cat > "$SCRIPT_DIR/requirements.txt" << EOL
xarray>=2023.1.0
numpy>=1.22.0
pandas>=1.5.0
fsspec>=2023.1.0
gcsfs>=2023.1.0
requests>=2.28.0
matplotlib>=3.5.0
scipy>=1.8.0
netCDF4>=1.6.0
zarr>=2.14.0
dask>=2023.1.0
EOL

echo "Created requirements.txt file"

# Check if the environment already exists
if [ -d "$ENV_DIR" ]; then
    echo "Environment already exists at $ENV_DIR"
    echo "Would you like to recreate it? [y/N]"
    read -r RECREATE
    if [[ $RECREATE =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        rm -rf "$ENV_DIR"
    else
        echo "Using existing environment"
    fi
fi

# Create the environment if it doesn't exist
if [ ! -d "$ENV_DIR" ]; then
    echo "Creating new Python virtual environment..."
    python3 -m venv "$ENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create Python virtual environment"
        exit 1
    fi
fi

# Activate the environment
echo "Activating environment..."
source "$ENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate environment"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

# Make scripts executable
chmod +x "$SCRIPT_DIR/scripts/era5_download.py"
chmod +x "$SCRIPT_DIR/scripts/era5_visualize.py"

echo ""
echo "=== Setup Complete ==="
echo "The ERA5 Tool has been set up successfully!"
echo ""
echo "To use the tool:"
echo "1. Activate the environment with: source $ENV_NAME/bin/activate"
echo "2. Download data with: python scripts/era5_download.py --year 2023 --month 1 --day 1 [options]"
echo "3. Visualize data with: python scripts/era5_visualize.py path/to/file.nc"
echo ""
echo "For more information, see the README.md and docs directory."

# Create data and plots directories
mkdir -p "$SCRIPT_DIR/data"
mkdir -p "$SCRIPT_DIR/plots"

# Deactivate the environment
deactivate