import RPi.GPIO as GPIO
import time
    #using the GPIO numbering system
GPIO.setmode(GPIO.BCM)


        #actual pin on the board trigger pin is 12 and echo pin is 18
GPIO_trigger=18;
GPIO_echo=24;

        #setting the pin operation
GPIO.setup(GPIO_trigger,GPIO.OUT);
GPIO.setup(GPIO_echo,GPIO.IN);
def dist():
        #setting the trigger high
    GPIO.output(GPIO_trigger,True);

        #setting of the trigger pin after the .01ms
    time.sleep(.00001);
    GPIO.output(GPIO_trigger,False);

    starttime=time.time()
    stoptime=time.time()

        #saving the start time
    while GPIO.input(GPIO_echo)==0:
        starttime=time.time()

        #saving the stop time
    while GPIO.input(GPIO_echo)==1:
        stoptime=time.time()

        #calculating the distance
    totaltime=stoptime-starttime;
    distance=(totaltime*34300)/2;
    return int(distance)


print(33-(dist()));

    

        
