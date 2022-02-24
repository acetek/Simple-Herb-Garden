import RPi.GPIO as GPIO
import time
import math
from ADCDevice import *
from datetime import datetime
GPIO.setmode(GPIO.BCM)

# Init Pump List with PIN Numbers
pinList = [4, 5, 6, 17]

#Loop and set Pump PINS to High
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

#Set time for pump to run


# main loop

adc = ADCDevice() # Define an ADCDevice class object

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)

def loop():
    while True:
        now = datetime.now()
        dt_string = now.strftime("%d %B, %Y, %H:%M:%S")
        #Setup Variables
        SleepTimeL = 4                         # Time for pump to run
        M0value = adc.analogRead(0)/214        # read ADC value A0 pin
        M1value = adc.analogRead(1)/214        # read ADC value A1 pin
        M2value = adc.analogRead(2)/214        # read ADC value A2 pin
        M0Percentage = "{:.2%}".format(M0value)
        M1Percentage = "{:.2%}".format(M1value)
        M2Percentage = "{:.2%}".format(M2value)
        print (dt_string + ("\n   Cilantro  Needing Water - %s - %s \n   Basil     Needing Water - %s - %s \n   Mint      Needing Water - %s - %s" %(M0Percentage,M0value,M1Percentage,M1value,M2Percentage,M2value)))
        if (M0value > .80):
            GPIO.output(4, GPIO.LOW)
            print ("Watering Cilantro...")
            time.sleep(SleepTimeL);
            GPIO.output(4, GPIO.HIGH)
        elif (M1value > .80):
            GPIO.output(6, GPIO.LOW)
            print ("Watering Basil...")
            time.sleep(SleepTimeL);
            GPIO.output(6, GPIO.HIGH)
        elif (M2value > .80):
            GPIO.output(17, GPIO.LOW)
            print ("Watering Mint...")
            time.sleep(SleepTimeL);
            GPIO.output(17, GPIO.HIGH)
        else:
            pass
        time.sleep(30.0)



def destroy():
    adc.close()
    GPIO.cleanup()

if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()