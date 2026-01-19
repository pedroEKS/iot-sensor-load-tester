import os

# MQTT Broker cfg
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "sensors/telemetry")

# Load Configuration
NUM_SENSORS = int(os.getenv("NUM_SENSORS", 10000))       # Total number of sensors
INTERVAL_SECONDS = float(os.getenv("INTERVAL_SECONDS", 5.0))    # Transmission interval 
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 500))          # Sensors started per batch
