import paho.mqtt.client as mqtt
from mqtt import *

def publisher(message: str, player, topic= "update"):
    broker_address = "192.168.2.23"  
    client = mqtt.Client(client_id="Publisher" + str(player), protocol=mqtt.MQTTv311)
    client.connect(broker_address, 1883, 60)
    client.publish(topic, message)

