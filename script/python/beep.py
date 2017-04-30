import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
channel=11
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, 3000)
p.start(0)

time.sleep(2)

def beep(seconds):
	p.ChangeDutyCycle(10)
	time.sleep(seconds)
	p.ChangeDutyCycle(0)

try:
	print("start")
	while True:
		beep(1)
		print("beep")
		time.sleep(5)
except:
        GPIO.cleanup()
