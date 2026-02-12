#!/bin/bash
# Launcher script for MapsCut on Linux/macOS

echo "Starting MapsCut..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -d "venv/lib/python*/site-packages/PyQt6" ]; then
    echo "Installing dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        echo
        echo "Some packages like GDAL may require additional installation steps."
        echo "Please see README.md for more information."
        exit 1
    fi
fi

# Run the application
echo
echo "Launching MapsCut..."
python main.py

# Deactivate virtual environment
deactivate
