import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM);
solenoid_valve=10
GPIO.setup(solenoid_valve,GPIO.OUT);
t_end=time.time()+2
GPIO.output(solenoid_valve,False);
while (time.time()<t_end):
    ans=1
#GPIO.output(solenoid_valve,False);
