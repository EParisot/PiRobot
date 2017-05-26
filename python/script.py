import webiopi
import datetime
import subprocess
from time import sleep

GPIO = webiopi.GPIO

NIGHT = 26

MOT1a = 5
MOT1b = 6
MOT2a = 12
MOT2b = 13


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

# # loop function is repeatedly called by WebIOPi 
# def loop():
	# # gives CPU some time before looping again
	# webiopi.sleep(1)


# destroy function is called at WebIOPi shutdown
def destroy():
	GPIO.setFunction(MOT1a, GPIO.IN)
	GPIO.setFunction(MOT1b, GPIO.IN)
	GPIO.setFunction(MOT2a, GPIO.IN)
	GPIO.setFunction(MOT2b, GPIO.IN)

