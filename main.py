import pandas as pd
import RPi.GPIO as GPIO  
from hx711 import HX711
import time as t
import Ultrasonic as u
GPIO.setmode(GPIO.BCM);
GPIO_trigger=18;
maxtime=40;
GPIO_echo=24;
button500=2;
button1000=3;
solenoid_valve=10
water_sensor=27
GPIO.setup(GPIO_trigger,GPIO.OUT);
GPIO.setup(GPIO_echo,GPIO.IN);
GPIO.setup(solenoid_valve,GPIO.OUT);
GPIO.setup(button500,GPIO.IN,pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(button1000,GPIO.IN,pull_up_down=GPIO.PUD_DOWN);
GPIO.setup(water_sensor,GPIO.IN);
offset=34
hx = HX711(dout_pin=5, pd_sck_pin=6)
err = hx.zero()
reading = hx.get_raw_data_mean()
plastic=pd.read_csv("/home/pi/HX711_Python3/data.csv")
height=plastic.Height.tolist()
weight=plastic.Weight.tolist()
time=plastic.Time.tolist()
if reading:
    print('Data subtracted by offset but still not converted to units:',
              reading)
else:
    print('invalid data', reading)
input('Put known weight on the scale and then press Enter')
reading = hx.get_data_mean()
if reading:
    print('Mean value from HX711 subtracted by offset:', reading)
    known_weight_grams = input('Write how many grams it was and press Enter: ')
    value = int(known_weight_grams)
    ratio = reading/value
    hx.set_scale_ratio(ratio)
def dist():
        #setting the trigger high
    GPIO.output(GPIO_trigger,True);

        #setting of the trigger pin after the .01ms
    GPIO.output(GPIO_trigger,False);

    starttime=t.time()
    stoptime=t.time()

        #saving the start time
    while GPIO.input(GPIO_echo)==0:
        starttime=t.time()

        #saving the stop time
    while GPIO.input(GPIO_echo)==1:
        stoptime=t.time()

        #calculating the distance
    totaltime=stoptime-starttime;
    distance=(totaltime*34300)/2;
    return int(distance)
def fillbottle(we,ti,mati,iniwe):
    time_on=ti-int((iniwe*ti)/we);
    if time_on>=mati:
        time_on=mati;
    t_end=t.time()+time_on;
    GPIO.output(solenoid_valve,True);
    while (t.time()<t_end):
        if GPIO.input(water_sensor)==0:
            break;
    GPIO.output(solenoid_valve,False);   
def adddata(he,wei,maxt):
    global maxtime
    global plastic;
    global height;
    global weight;
    global time;
    t_start=t.time();
    t_end=t.time()+maxtime;
    GPIO.output(solenoid_valve,True);
    while (t.time()<t_end):
        if GPIO.input(water_sensor)==0:
            GPIO.output(solenoid_valve,False);
            break;
    GPIO.output(solenoid_valve,False);
    time_total=t.time()-t_start-5;
    list1=[]
    list1.append(he);
    wei=int(hx.get_weight_mean(20));
    list1.append(wei-10);
    list1.append(int(time_total));
    plastic=plastic.append(pd.DataFrame([list1],columns=['Height','Weight','Time']),ignore_index=True)
    plastic.to_csv("/home/pi/HX711_Python3/data.csv");
    list1[0]=list1[0]-1;
    plastic=plastic.append(pd.DataFrame([list1],columns=['Height','Weight','Time']),ignore_index=True)
    plastic.to_csv("/home/pi/HX711_Python3/data.csv");
    list1[0]=list1[0]+1;
    plastic=plastic.append(pd.DataFrame([list1],columns=['Height','Weight','Time']),ignore_index=True)
    plastic.to_csv("/home/pi/HX711_Python3/data.csv");
    list1[0]=list1[0]-2;
    plastic=plastic.append(pd.DataFrame([list1],columns=['Height','Weight','Time']),ignore_index=True)
    plastic.to_csv("/home/pi/HX711_Python3/data.csv");
    list1[0]=list1[0]+2;
    plastic=plastic.append(pd.DataFrame([list1],columns=['Height','Weight','Time']),ignore_index=True)
    plastic.to_csv("/home/pi/HX711_Python3/data.csv");
#input("Please Enter");    
while(True):
    input("Please Enter");
    maxtime=100;
##    while True:
##        if(dist()<30):
##            print(dist())
##            maxtime=100
##            break;
##            if GPIO.input(button500)==1:
##                maxtime=40
##                break;
##            elif GPIO.input(button1000)==1:
##                maxtime=40
##                break;    
    hob=int(offset-dist());
    print(hob)
    iniweight=int(hx.get_weight_mean(20))
    print(iniweight)
    try:
        n=height.index(hob);
        print("h")
        fillbottle(weight[n],time[n],maxtime,iniweight)
    except ValueError as error:
        adddata(hob,iniweight,maxtime);
        
        
        
    
    
    

    
