import webiopi
import datetime
import subprocess
from time import sleep
from gpiozero import DistanceSensor

GPIO = webiopi.GPIO

NIGHT = 26

MOT1v = 12
MOT1a = 13
MOT1b = 19

MOT2v = 16
MOT2a = 20
MOT2b = 21

ultrasonic = DistanceSensor(echo=24, trigger=23)

global temp

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
	
@webiopi.macro
def Temp(arg0):
	global temp
	temp = int(subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])[5:7])
	print (temp)
	return ("%s" % (temp))


# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used	
	GPIO.setFunction(MOT1a, GPIO.OUT)
	GPIO.digitalWrite(MOT1a, GPIO.LOW)
	GPIO.setFunction(MOT1b, GPIO.OUT)
	GPIO.digitalWrite(MOT1b, GPIO.LOW)
	GPIO.setFunction(MOT2a, GPIO.OUT)
	GPIO.digitalWrite(MOT2a, GPIO.LOW)
	GPIO.setFunction(MOT2b, GPIO.OUT)
	GPIO.digitalWrite(MOT2b, GPIO.LOW)
	GPIO.setFunction(MOT1v, GPIO.PWM)
	GPIO.pulseRatio(MOT1v, 0)
	GPIO.setFunction(MOT2v, GPIO.PWM)
	GPIO.pulseRatio(MOT2v, 0)

# loop function is repeatedly called by WebIOPi 
#def loop():
##        dist = ultrasonic.distance
##        if (dist < 0.300000):
##                GPIO.pulseRatio(19, 1)
##                GPIO.pulseRatio(13, 1)
##                GPIO.pulseRatio(21, 1)
##                GPIO.pulseRatio(20, 1)
##                sleep(2)
##                GPIO.pulseRatio(19, 0)
##                GPIO.pulseRatio(13, 0)
##                GPIO.pulseRatio(21, 0)
##                GPIO.pulseRatio(20, 0)
##                sleep(3)
##        elif (dist > 0.700000):
##                GPIO.pulseRatio(19, 1)
##                GPIO.pulseRatio(13, 1)
##                GPIO.pulseRatio(21, 1)
##                GPIO.pulseRatio(20, 1)
##                sleep(2)
##                GPIO.pulseRatio(19, 0)
##                GPIO.pulseRatio(13, 0)
##                GPIO.pulseRatio(21, 0)
##                GPIO.pulseRatio(20, 0)
##                sleep(3)
#        sleep(0.1)

# destroy function is called at WebIOPi shutdown
def destroy():
	GPIO.digitalWrite(MOT1a, GPIO.LOW)
	GPIO.digitalWrite(MOT1b, GPIO.LOW)
	GPIO.setFunction(MOT1v, GPIO.OUT)
	GPIO.digitalWrite(MOT1v, GPIO.LOW)
	
	GPIO.digitalWrite(MOT2a, GPIO.LOW)
	GPIO.digitalWrite(MOT2b, GPIO.LOW)
	GPIO.setFunction(MOT2v, GPIO.OUT)
	GPIO.digitalWrite(MOT2v, GPIO.LOW)
