import webiopi
import datetime
from time import sleep
import subprocess
from gpiozero import DistanceSensor


GPIO = webiopi.GPIO

NIGHT = 26

MOT1v = 12
MOT1a = 13
MOT1b = 19
MOT2v = 16
MOT2a = 20
MOT2b = 21

ultrasonic = DistanceSensor(echo=17, trigger=4)
led1 = 24
led2 = 23
led3 = 18


global temp


##@webiopi.macro
##def GoogleOn():		
##	subprocess.Popen(["/bin/bash", "/home/pi/GA.sh"])


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
	return (temp)

def Distance():
        dist = ultrasonic.distance
        return (dist)


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
	
	GPIO.setFunction(led1, GPIO.OUT)
	GPIO.digitalWrite(led1, GPIO.LOW)
	GPIO.setFunction(led2, GPIO.OUT)
	GPIO.digitalWrite(led2, GPIO.LOW)
	GPIO.setFunction(led3, GPIO.OUT)
	GPIO.digitalWrite(led3, GPIO.LOW)

# loop function is repeatedly called by WebIOPi 
##def loop():        
##        if Distance() < 0.3000000:
##                GPIO.digitalWrite(led1, GPIO.HIGH)
##                sleep(1)
##        elif Distance() < 0.5000000:
##                GPIO.digitalWrite(led2, GPIO.HIGH)
##                sleep(1)
##        else:
##                GPIO.digitalWrite(led3, GPIO.HIGH)
##                sleep(1)
##        GPIO.digitalWrite(led1, GPIO.LOW)
##        GPIO.digitalWrite(led2, GPIO.LOW)
##        GPIO.digitalWrite(led3, GPIO.LOW)
##        webiopi.sleep(1)

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
	
	GPIO.digitalWrite(led1, GPIO.LOW)
	GPIO.digitalWrite(led2, GPIO.LOW)
	GPIO.digitalWrite(led3, GPIO.LOW)
