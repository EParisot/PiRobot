import webiopi
import datetime
import subprocess
from time import sleep
from gpiozero import DistanceSensor

GPIO = webiopi.GPIO

NIGHT = 26

MOT1a = 2
MOT1b = 3
MOT2a = 4
MOT2b = 17


ultrasonic = DistanceSensor(echo=24, trigger=23)

@webiopi.macro
def camOn():		
	subprocess.call('sudo service livestream.sh start', shell=True)		

@webiopi.macro
def camOff():
	subprocess.call('sudo service livestream.sh stop', shell=True)

@webiopi.macro
def takeaPic():
	picdate = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	piccmd = 'wget http://192.168.3.1:8080/?action=snapshot -O /home/pi/Pictures/Photos/' + picdate + '.jpg'
	subprocess.call(piccmd, shell=True)

# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used	
	GPIO.setFunction(MOT1a, GPIO.PWM)
	GPIO.setFunction(MOT1b, GPIO.PWM)
	GPIO.setFunction(MOT2a, GPIO.PWM)
	GPIO.setFunction(MOT2b, GPIO.PWM)

# loop function is repeatedly called by WebIOPi 
def loop():
        dist = ultrasonic.distance
        if ((dist > 0.300000) and (dist < 0.700000)):
                sleep(0.1)
        elif (dist < 0.300000):
                GPIO.pulseRatio(2, 1)
                GPIO.pulseRatio(3, 1)
                GPIO.pulseRatio(4, 1)
                GPIO.pulseRatio(17, 1)
                sleep(2)
                GPIO.pulseRatio(2, 0)
                GPIO.pulseRatio(3, 0)
                GPIO.pulseRatio(4, 0)
                GPIO.pulseRatio(17, 0)
                sleep(1)
        elif (dist > 0.700000):
                GPIO.pulseRatio(2, 1)
                GPIO.pulseRatio(3, 1)
                GPIO.pulseRatio(4, 1)
                GPIO.pulseRatio(17, 1)
                sleep(2)
                GPIO.pulseRatio(2, 0)
                GPIO.pulseRatio(3, 0)
                GPIO.pulseRatio(4, 0)
                GPIO.pulseRatio(17, 0)
                sleep(1)

# destroy function is called at WebIOPi shutdown
def destroy():
	GPIO.setFunction(MOT1a, GPIO.OUT)
	GPIO.setFunction(MOT1b, GPIO.OUT)
	GPIO.setFunction(MOT2a, GPIO.OUT)
	GPIO.setFunction(MOT2b, GPIO.OUT)

