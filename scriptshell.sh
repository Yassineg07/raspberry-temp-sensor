#!/bin/bash

# Set strict error handling
set -euo pipefail

# Configuration variables
I2C_BUS="/sys/bus/i2c/devices/i2c-1"
I2C_DEVICE="${I2C_BUS}/1-0038"
AHT10_ADDRESS="0x38"
SCRIPT_PYTHON="/home/aht10/aht10.py"

# Function to log messages with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_message "Error: Please run as root"
        exit 1
    fi
}

# Function to load required modules
load_modules() {
    log_message "Loading I2C and AHT10 modules..."
    modprobe i2c-dev || { log_message "Failed to load i2c-dev module"; exit 1; }
    modprobe aht10 || { log_message "Failed to load aht10 module"; exit 1; }
}

# Function to initialize AHT10 device
init_aht10() {
    log_message "Configuring AHT10 device on I2C bus..."
    
    if [ ! -d "$I2C_BUS" ]; then
        log_message "Error: I2C bus not found!"
        exit 1
    fi

    log_message "Adding AHT10 device at ${AHT10_ADDRESS}..."
    echo "aht10 ${AHT10_ADDRESS}" | tee "${I2C_BUS}/new_device"

    # Wait for device initialization
    sleep 2

    if [ ! -d "$I2C_DEVICE" ]; then
        log_message "Error: Failed to initialize AHT10 device"
        exit 1
    fi
    
    log_message "AHT10 device initialized successfully"
}

# Function to run Python script
run_python_script() {
    if [ ! -f "$SCRIPT_PYTHON" ]; then
        log_message "Error: Python script not found at ${SCRIPT_PYTHON}"
        exit 1
    fi

    log_message "Running Python script to read AHT10 data and send to MQTT..."
    python3 "$SCRIPT_PYTHON"
}

# Main execution
main() {
    check_root
    load_modules
    init_aht10
    run_python_script
}

# Run main function
main