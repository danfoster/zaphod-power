import asyncio
import logging
import paho.mqtt.client as mqtt
import os
import json

logger = logging.getLogger(__name__)


MQTT_HOST=os.getenv("MQTT_HOST", "localhost")
TOPIC_SUB=os.getenv("TOPIC_SUB", "plug/tasmota_dan_zaphod_D5E82D/tele/SENSOR")
TOPIC_PUB=os.getenv("TOPIC_PUB", "server/dan-zaphod/power")

def get_power(payload):
    j = json.loads(payload)
    try:
        return int(j["ENERGY"]["Power"])
    except KeyError:
        logger.warning(f"Got unpexcted payload: {j}")
        return 0

def on_message(client, username, msg):
    power = get_power(msg.payload)
    logger.info(f"Publishing to {TOPIC_PUB}: {power}")
    client.publish(TOPIC_PUB, power)

def main():
    logging.basicConfig(level=logging.INFO)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_HOST)
    client.subscribe(TOPIC_SUB)
    logger.info("Starting...")
    client.loop_forever()


if __name__=="__main__":
    main()