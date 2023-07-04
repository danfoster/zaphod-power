from meross_iot.http_api import MerossHttpClient
import asyncio
from meross_iot.manager import MerossManager
import logging
import paho.mqtt.client as mqtt 
import os

logger = logging.getLogger(__name__)

EMAIL = "dan@zem.org.uk"
PASSWORD = os.environ.get("MEROSS_PASS")

def main():
    logger.root.setLevel(logging.WARNING)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
    loop.stop()
    
    
async def async_main():
    http_api_client = await MerossHttpClient.async_from_user_password(EMAIL, PASSWORD)
    
     # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    device = await get_device(manager, "zaphod")
    client = mqtt.Client()
    client.connect("mqtt.hacklab") 
    
    while True:
        instant_consumption = await device.async_get_instant_metrics()
        
        print(f"Power: {instant_consumption.power}")
        client.publish("server/dan-zaphod/power", instant_consumption.power)
        await asyncio.sleep(30)

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()
    
    
async def get_device(manager, device_name):
    # Discover devices.
    await manager.async_device_discovery()
    meross_devices = manager.find_devices()
    
    
    for dev in meross_devices:
        if dev.name == device_name:
            return dev
    
    raise Exception(f"No device called {device_name} found")
      

    
if __name__=="__main__":
    main()