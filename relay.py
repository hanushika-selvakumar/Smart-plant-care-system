import RPi.GPIO as GPIO
from time import sleep

relay_water = 21
relay_plant = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_water, GPIO.OUT)
GPIO.setup(relay_plant, GPIO.OUT)

while 1:
    GPIO.output(relay_plant, GPIO.HIGH)
    sleep(1)
    GPIO.output(relay_plant, GPIO.LOW)
    sleep(1)
    GPIO.output(relay_water, GPIO.HIGH)
    sleep(1)
    GPIO.output(relay_water, GPIO.LOW)
    sleep(1)
