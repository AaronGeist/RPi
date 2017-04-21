import RPi.GPIO as GPIO
import time


class Servo:
    duty_cycle = 0
    step = 10
    pin = None

    @staticmethod
    def initialize():
        if Servo.pin is None:
            Servo.duty_cycle = 7.5
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT, initial=False)
            Servo.pin = GPIO.PWM(17, 50)  # 50HZ
            Servo.pin.start(0)

    @staticmethod
    def left():
        Servo.initialize()
        Servo.duty_cycle += 0.5
        Servo.duty_cycle = min(Servo.duty_cycle, 12.5)
        print(Servo.duty_cycle)
        Servo.pin.ChangeDutyCycle(Servo.duty_cycle)
        time.sleep(0.02)
        Servo.pin.ChangeDutyCycle(0)
        time.sleep(0.05)

    @staticmethod
    def right():
        Servo.initialize()
        Servo.duty_cycle -= 0.5
        Servo.duty_cycle = max(Servo.duty_cycle, 2.5)
        print(Servo.duty_cycle)
        Servo.pin.ChangeDutyCycle(Servo.duty_cycle)
        time.sleep(0.02)
        Servo.pin.ChangeDutyCycle(0)
        time.sleep(0.05)

if __name__ == "__main__":
	Servo.left();
	Servo.left();
	Servo.left();
	Servo.left();
	Servo.left();
	Servo.right();
	Servo.right();
	Servo.right();
	Servo.right();
	Servo.right();
