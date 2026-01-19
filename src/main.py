import asyncio
import json
import random
import time
import sys
import os
import logging
from datetime import datetime
from aiomqtt import Client
from faker import Faker
import config

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Inicializa gerador de dados falsos
fake = Faker()

# --- CORREÇÃO OBRIGATÓRIA PARA WINDOWS ---
# O ProactorEventLoop (padrão do Windows) não suporta add_reader/writer
# que o aiomqtt usa. Precisamos forçar o SelectorEventLoop.
if sys.platform.lower() == "win32" or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# -----------------------------------------

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
                    logger.info(f"Sensor {sensor_id} sent data: {payload['value']}")
                
                # Await interval before next transmission | Simulates real-time delay
                await asyncio.sleep(config.INTERVAL_SECONDS)
                
    except Exception as e:
        logger.error(f"Sensor {sensor_id} failed: {e}")

async def main():
    logger.info(f"--- STARTING LOAD TEST: {config.NUM_SENSORS} SENSORS ---")
    logger.info(f"Target: {config.MQTT_BROKER}:{config.MQTT_PORT}")
    
    tasks = []
    
    # Create sensors in batches to avoid initial CPU spike (ramp-up)
    for i in range(config.NUM_SENSORS):
        tasks.append(simulate_sensor(i))
        
        if i % config.BATCH_SIZE == 0:
            await asyncio.sleep(0.5)  # Brief pause to stabilize
            logger.info(f"[SYSTEM] {i} sensors initialized...")

    # Keep all tasks running indefinitely
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        # Main Asyncio Loop
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n[SYSTEM] Test stopped by user.")