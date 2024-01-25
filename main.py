import sys
from Adafruit_IO import MQTTClient

import time
import random

AIO_FEED_IDs = ["led", "pump"]
AIO_USERNAME = "MTPQ_BKU"
AIO_KEY = "aio_KgJT68eV93xf9gaUnGpMXeWEErnA"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + ", feed id: " + feed_id)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

counter = 10

while True:
    counter = counter - 1
    if counter <= 0:
        counter = 10

        temp = random.randint(20, 60)
        client.publish("temperature", temp)
        humi = random.randint(50, 70)
        client.publish("humidity", humi)
        light = random.randint(500, 1500)
        client.publish("light", light)

    time.sleep(1)
    pass
