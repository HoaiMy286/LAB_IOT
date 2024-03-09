import sys
import cv2  # Install opencv-python
import os
from Adafruit_IO import MQTTClient
from simple_ai import *
from uart import *

import time
import random

AIO_FEED_IDs = ["led", "pump"]
AIO_USERNAME = "MTPQ_BKU"
AIO_KEY = "aio_tkHs40fn5WDpsNUJD9sa2ZlRIdYW"

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
    if feed_id == "led":
        if payload == "0":  # OFF
            writeData("Led_OFF") 
        else:               # ON
            writeData("Led_ON")
    if feed_id == "pump":
        if payload == "0":  # OFF
            writeData("Pump_OFF") 
        else:               # ON
            writeData("Pump_ON")

# ////////////// WSL /////////////
#  def message(client , feed_id , payload):
#     print("Nhan du lieu: " + payload + ", feed id: " + feed_id)
#     if feed_id == "led":
#         if payload == "0":  # OFF
#             os.system("echo \"LED_OFF\" > /dev/pts/4")
#         else:               # ON
#             os.system("echo \"LED_ON\" > /dev/pts/4")
#     if feed_id == "pump":
#         if payload == "0":  # OFF
#             os.system("echo \"PUMP_OFF\" > /dev/pts/4")
#         else:               # ON
#             os.system("echo \"PUMP_ON\" > /dev/pts/4")       

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
