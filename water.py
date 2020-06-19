import RPi.GPIO as GPIO
import os
GPIO.setmode(GPIO.BCM)
water_sensor=27
GPIO.setup(water_sensor,GPIO.IN);
while(True):
    if GPIO.input(water_sensor)==0:
        print("Water")
