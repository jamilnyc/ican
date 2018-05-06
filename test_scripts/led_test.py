import RPi.GPIO as GPIO
import time

pinNum = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinNum, GPIO.OUT)
print "turning on"
GPIO.output(pinNum, True)
print "Sleeping for 30"
time.sleep(30)
print "Turning off"
GPIO.output(pinNum, False)
GPIO.cleanup()

# import gpiozero
#
# led = gpiozero.LED(pinNum)
# led.on()
# time.sleep(20)
# led.off()
