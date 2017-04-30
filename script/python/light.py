import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN )

try:
	while True:
		if GPIO.input(37) == GPIO.LOW:
			print("low")
		else:
			print("high")
		time.sleep(1)

except:
	GPIO.cleanup()




