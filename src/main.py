import asyncio
import json
import random
import time
from datetime import datetime
from aiomqtt import Client
from faker import Faker
import config

# Initialize fake data generator
fake = Faker()

async def simulate_sensor(sensor_id):
    """
    Simulates a single IoT sensor that connects, sends data, and sleeps.
    """
    # Create varied data types to mimic real scenarios
    device_type = random.choice(["thermometer", "vibration", "pressure"])
    
    try:
        async with Client(config.MQTT_BROKER, port=config.MQTT_PORT) as client:
            while True:
                # Telemetry JSON payload
                payload = {
                    "sensor_id": f"sensor_{sensor_id}",
                    "type": device_type,
                    "value": round(random.uniform(20.0, 100.0), 2),
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "active"
                }
                
                # Publish to MQTT topic
                await client.publish(config.MQTT_TOPIC, payload=json.dumps(payload))
                
                # Reduced logging to avoid terminal clutter -- shows only every 1000th sensor
                if sensor_id % 1000 == 0:
                    print(f"[DEBUG] Sensor {sensor_id} sent data: {payload['value']}")
                
                # Await interval before next transmission | Simulates real-time delay
                await asyncio.sleep(config.INTERVAL_SECONDS)
                
    except Exception as e:
        print(f"[ERROR] Sensor {sensor_id} failed: {e}")

async def main():
    print(f"--- STARTING LOAD TEST: {config.NUM_SENSORS} SENSORS ---")
    print(f"Target: {config.MQTT_BROKER}:{config.MQTT_PORT}")
    
    tasks = []
    
    # Create sensors in batches to avoid initial CPU spike (ramp-up)
    for i in range(config.NUM_SENSORS):
        tasks.append(simulate_sensor(i))
        
        if i % config.BATCH_SIZE == 0:
            await asyncio.sleep(0.5)  # Brief pause to stabilize
            print(f"[SYSTEM] {i} sensors initialized...")

    # Keep all tasks running indefinitely
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        # Main Asyncio Loop
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SYSTEM] Test stopped by user.")