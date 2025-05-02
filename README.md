# Raspberry Temperature Sensor

A Raspberry Pi-based temperature and humidity monitoring system using the AHT10 sensor. This project reads sensor data and publishes it to an MQTT broker for further processing or visualization.

## Features

- Reads temperature and humidity data from the AHT10 sensor.
- Publishes sensor data to an MQTT broker.
- Configurable and easy to set up.
- Includes a Bash script for initializing the sensor and running the Python script.

## Installation

### Prerequisites

- Raspberry Pi with I2C enabled.
- AHT10 sensor connected to the I2C bus.
- Python 3 installed on the Raspberry Pi.
- MQTT broker (e.g., Mosquitto) running on your network.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/raspberry-temp-sensor.git
   cd raspberry-temp-sensor
   ```

2. Install required Python dependencies:
   ```bash
   pip install paho-mqtt
   ```

3. Ensure the I2C kernel modules are loaded:
   ```bash
   sudo modprobe i2c-dev
   sudo modprobe aht10
   ```

4. Update the configuration in the Bash script (`scriptshell.txt`) and Python script (`aht10.py`) with your MQTT broker's IP address and other settings.

## Usage

1. Make the Bash script executable:
   ```bash
   chmod +x scriptshell.txt
   ```

2. Run the Bash script to initialize the sensor and start the Python script:
   ```bash
   sudo ./scriptshell.txt
   ```

3. The Python script will continuously read temperature and humidity data and publish it to the MQTT broker under the following topics:
   - Temperature: `sensor/aht10/temperature`
   - Humidity: `sensor/aht10/humidity`

4. Use an MQTT client or dashboard (e.g., MQTT Explorer) to monitor the published data.

## Configuration

- **MQTT Settings**: Update the `MQTT_BROKER` and `MQTT_PORT` variables in `aht10.py` with your broker's details.
- **Sensor Paths**: Ensure the file paths for temperature and humidity in `aht10.py` match your system's configuration.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue or contact [Yassineg07](mailto:gharbiyasine040@gmail.com).
