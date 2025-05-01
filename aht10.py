import time
import logging
from typing import Tuple, Optional
import paho.mqtt.client as mqtt

# MQTT connection settings
MQTT_BROKER = "IP.ADRESSE"  # IP address of the MQTT broker
MQTT_PORT = 1883            # Default MQTT port
MQTT_TOPIC_TEMP = "sensor/aht10/temperature"  # Topic for temperature readings
MQTT_TOPIC_HUMID = "sensor/aht10/humidity"    # Topic for humidity readings
SLEEP_DURATION = 2  # Time to wait between sensor readings (in seconds)

# File paths for reading sensor data from the Linux filesystem
# These files contain the raw sensor values provided by the AHT10 driver
TEMP_PATH = "/sys/bus/i2c/devices/i2c-1/1-0038/hwmon/hwmon2/temp1_input"
HUMID_PATH = "/sys/bus/i2c/devices/i2c-1/1-0038/hwmon/hwmon2/humidity1_input"

# Setup logging configuration to track program execution and errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_sensor_data() -> Tuple[Optional[float], Optional[float]]:
    """Read temperature and humidity from AHT10 sensor.
    The sensor values are read from system files and converted from millidegrees/millipercent to actual values.

    Returns:
        tuple: (temperature, humidity) or (None, None) if error occurs
    """
    try:
        # Read and convert temperature (divide by 1000 to convert from millidegrees to degrees)
        with open(TEMP_PATH, "r") as temp_file:
            temperature = int(temp_file.read().strip()) / 1000.0
        # Read and convert humidity (divide by 1000 to convert from millipercent to percent)
        with open(HUMID_PATH, "r") as humid_file:
            humidity = int(humid_file.read().strip()) / 1000.0
        return temperature, humidity
    except FileNotFoundError:
        logging.error("Sensor data files not found!")
        return None, None
    except ValueError as e:
        logging.error(f"Error reading sensor data: {e}")
        return None, None

def setup_mqtt() -> mqtt.Client:
    """Initialize and connect to the MQTT broker.
    This allows us to publish sensor data to the network.

    Returns:
        mqtt.Client: Connected MQTT client
    """
    # Create a new MQTT client instance
    client = mqtt.Client()
    try:
        # Attempt to connect to the MQTT broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)  # 60 seconds keepalive
        logging.info("Connected to MQTT broker")
        return client
    except Exception as e:
        logging.error(f"Failed to connect to MQTT broker: {e}")
        raise

def main():
    """Main program loop that continuously reads sensor data and publishes to MQTT."""
    # Initialize MQTT connection
    client = setup_mqtt()
    
    try:
        # Continuous loop to read and publish sensor data
        while True:
            # Read current temperature and humidity values
            temperature, humidity = read_sensor_data()
            
            # Only publish if we have valid readings
            if temperature is not None and humidity is not None:
                logging.info(f"Temperature: {temperature}°C, Humidity: {humidity}%")
                
                try:
                    # Publish readings to respective MQTT topics
                    client.publish(MQTT_TOPIC_TEMP, temperature)
                    client.publish(MQTT_TOPIC_HUMID, humidity)
                    logging.debug("Data published to MQTT")
                except Exception as e:
                    logging.error(f"Failed to publish to MQTT: {e}")
            
            # Wait before next reading
            time.sleep(SLEEP_DURATION)
    except KeyboardInterrupt:
        # Handle clean shutdown on Ctrl+C
        logging.info("Script interrupted by user")
    finally:
        # Ensure MQTT connection is properly closed
        client.disconnect()
        logging.info("MQTT client disconnected")

# Standard Python idiom to run the main function
if __name__ == "__main__":
    main()