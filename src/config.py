# MQTT Broker cfg
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/telemetry"

# Load Configuration
NUM_SENSORS = 10000       # Total number of sensors
INTERVAL_SECONDS = 5.0    # Transmission interval (seconds)
BATCH_SIZE = 500          # Sensors started per batch | to avoid blowing up the CPU at start =)