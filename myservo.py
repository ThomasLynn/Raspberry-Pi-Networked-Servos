import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, 50) # GPIO 17 for PWM with 50Hz
        self.p.start(2.5) # Initialization
        
        self.starting_angle = None

    def set_angle(self, angle):
        norm = angle / 180.0
        self.p.ChangeDutyCycle(norm * 8.4 + 2.2)
        
        if self.starting_angle == None:
            delta = 180
        else:
            delta = abs(self.starting_angle - angle)
        time.sleep(delta * 0.4 / 180 + 0.05)
        self.starting_angle = angle
        
        self.p.ChangeDutyCycle(0)

    def freeze_angle(self):
        self.p.ChangeDutyCycle(0)

    def stop(self):
        self.p.stop()
        GPIO.cleanup()
