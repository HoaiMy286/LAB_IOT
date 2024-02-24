import sys
import cv2  # Install opencv-python
from Adafruit_IO import MQTTClient
from simple_ai import *
from uart import *

import time
import random

AIO_FEED_IDs = ["led", "pump"]
AIO_USERNAME = "MTPQ_BKU"
AIO_KEY = "aio_tSsv49W5tPo42LVjwsSYnGlPpgte"

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
sensor_type = 0

counter_ai = 5
ai_result = ""
previous_ai_result = ""

while True:
    # counter = counter - 1
    # if counter <= 0:
    #     counter = 10

    #     if sensor_type == 0:
    #         print("Temperature...")
    #         temp = random.randint(20, 60)
    #         client.publish("temperature", temp)
    #         sensor_type = 1
    #     elif sensor_type == 1:
    #         print("Humidity")
    #         humi = random.randint(50, 70)
    #         client.publish("humidity", humi)
    #         sensor_type = 2
    #     elif sensor_type == 2:
    #         print("Light...")
    #         light = random.randint(500, 1500)
    #         client.publish("light", light)
    #         sensor_type = 0
  
    readSerial(client)

    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5

        previous_ai_result = ai_result
        ai_result = image_detector()
        print("AI Output: ", ai_result)

        if ai_result != previous_ai_result:
            client.publish("ai", ai_result)

    time.sleep(1)

    # Listen to the keyboard for presses.
    # keyboard_input = cv2.waitKey(1)

    # # 27 is the ASCII for the esc key on your keyboard.
    # if keyboard_input == 27:
    #     break
