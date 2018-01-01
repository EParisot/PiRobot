import webiopi
import datetime
from time import sleep
import subprocess
from gpiozero import DistanceSensor, MotionSensor

# import opencv necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
# init camera and grab a ref to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.hflip = True
camera.vflip = True
rawCapture = PiRGBArray(camera, size=(640, 480))

GPIO = webiopi.GPIO

NIGHT = 26

MOT1v = 12
MOT1a = 19
MOT1b = 13
MOT2v = 16
MOT2a = 21
MOT2b = 20

led1 = 24
led2 = 23
led3 = 18

ultrasonic = DistanceSensor(echo=17, trigger=4)
pir = MotionSensor(27)


@webiopi.macro
def camOn():
	subprocess.call('sudo service livestream.sh start', shell=True)

@webiopi.macro
def camOff():
	subprocess.call('sudo service livestream.sh stop', shell=True)

@webiopi.macro
def takeaPic():
	picdate = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	piccmd = 'raspistill -vf -hf -o /home/pi/Pictures/Photos/' + picdate + '.jpg'
	subprocess.call(piccmd, shell=True)

@webiopi.macro
def Temp(arg0):
	temp = int(subprocess.check_output(["/opt/vc/bin/vcgencmd","measure_temp"])[5:7])
	return (temp)

@webiopi.macro
def Shutdown():
        subprocess.call(["sudo", "shutdown"])

@webiopi.macro
def Reboot():
        subprocess.call(["sudo", "reboot"])

def Distance():
        dist = ultrasonic.distance
        return (dist)

def avancer():
        GPIO.digitalWrite(MOT1b, GPIO.LOW)
        GPIO.digitalWrite(MOT2b, GPIO.LOW)
        GPIO.digitalWrite(MOT1a, GPIO.HIGH)
        GPIO.digitalWrite(MOT2a, GPIO.HIGH)
        GPIO.pulseRatio(MOT1v, 0.2)
        GPIO.pulseRatio(MOT2v, 0.2)

def rotateR():
        GPIO.digitalWrite(MOT1b, GPIO.HIGH)
        GPIO.digitalWrite(MOT1a, GPIO.LOW)
        GPIO.digitalWrite(MOT2b, GPIO.LOW)
        GPIO.digitalWrite(MOT2a, GPIO.HIGH)
        GPIO.pulseRatio(MOT1v, 0.4)
        GPIO.pulseRatio(MOT2v, 0.4)
        sleep(0.2)
        GPIO.pulseRatio(MOT1v, 0)
        GPIO.pulseRatio(MOT2v, 0)

def rotateL():
        GPIO.digitalWrite(MOT1a, GPIO.HIGH)
        GPIO.digitalWrite(MOT1b, GPIO.LOW)
        GPIO.digitalWrite(MOT2a, GPIO.LOW)
        GPIO.digitalWrite(MOT2b, GPIO.HIGH)
        GPIO.pulseRatio(MOT1v, 0.4)
        GPIO.pulseRatio(MOT2v, 0.4)
        sleep(0.2)
        GPIO.pulseRatio(MOT1v, 0)
        GPIO.pulseRatio(MOT2v, 0)

def reactionDistance():
        GPIO.digitalWrite(MOT1a, GPIO.LOW)
        GPIO.digitalWrite(MOT2a, GPIO.LOW)
        GPIO.digitalWrite(MOT1b, GPIO.HIGH)
        GPIO.digitalWrite(MOT2b, GPIO.HIGH)
        GPIO.pulseRatio(MOT1v, 0.4)
        GPIO.pulseRatio(MOT2v, 0.4)
        sleep(0.1)
        GPIO.pulseRatio(MOT1v, 0)
        GPIO.pulseRatio(MOT2v, 0)
        sleep(0.1)
        rotateR()

def scanFace():
        # allow camera to warm up
        time.sleep(0.1)
        
        # capture an image
        camera.capture(rawCapture, format='bgr')
        # At this point the image is available as stream.array
        img = rawCapture.array
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # import XML Classifiers
        face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.0/data/haarcascades/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
                GPIO.digitalWrite(led3, GPIO.HIGH)
                sleep(0.5)
                GPIO.digitalWrite(led3, GPIO.LOW)
                sleep(0.5)
        else:
                GPIO.digitalWrite(led1, GPIO.HIGH)
                sleep(0.5)
                GPIO.digitalWrite(led1, GPIO.LOW)
                sleep(0.5)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

def scanDistance():
        if Distance()<0.5000000:
                reactionDistance()
                GPIO.digitalWrite(led1, GPIO.HIGH)
                sleep(0.01)
        elif Distance()<1.0:
                GPIO.digitalWrite(led2, GPIO.HIGH)
                avancer()
                sleep(0.1)
        else:
                GPIO.digitalWrite(led3, GPIO.HIGH)
                avancer()
                sleep(0.2)
        GPIO.digitalWrite(led1, GPIO.LOW)
        GPIO.digitalWrite(led2, GPIO.LOW)
        GPIO.digitalWrite(led3, GPIO.LOW)

def searchMvt():
        if pir.motion_detected:
                takeaPic()
                GPIO.digitalWrite(led1, GPIO.HIGH)
                GPIO.digitalWrite(led2, GPIO.HIGH)
                GPIO.digitalWrite(led3, GPIO.HIGH)                
                sleep(1)
                GPIO.digitalWrite(led1, GPIO.LOW)
                GPIO.digitalWrite(led2, GPIO.LOW)
                GPIO.digitalWrite(led3, GPIO.LOW)
                sleep(1)


class Switch:
    def __init__(self, switch_state):
        self.switch_state = switch_state

switchDist = Switch(False)
switchMvt = Switch(False)


@webiopi.macro
def DistOn():
        switchDist.switch_state = True


@webiopi.macro
def DistOff():
        switchDist.switch_state = False
        GPIO.digitalWrite(MOT1a, GPIO.LOW)
        GPIO.digitalWrite(MOT2a, GPIO.LOW)
        GPIO.digitalWrite(MOT1b, GPIO.HIGH)
        GPIO.digitalWrite(MOT2b, GPIO.HIGH)
        GPIO.pulseRatio(MOT1v, 0)
        GPIO.pulseRatio(MOT2v, 0)
        


@webiopi.macro
def MvtOn():
        switchMvt.switch_state = True

@webiopi.macro
def MvtOff():
        switchMvt.switch_state = False



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



### loop function is repeatedly called by WebIOPi 
def loop():
        if switchDist.switch_state==True:
                #scanDistance()
                pass

        if  switchMvt.switch_state==True:
                #searchMvt()
                scanFace()

        webiopi.sleep(0.01)

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
