import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
# make io.input low when nothing connecting
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
	cnt = 0
	while True:
		if GPIO.input(35) == GPIO.LOW:
			print("low " + str(cnt))
		else:
			print("high " + str(cnt))
		cnt += 1
		time.sleep(1)

except:
	GPIO.cleanup()




