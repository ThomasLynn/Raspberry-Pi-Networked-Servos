import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, 50) # GPIO 17 for PWM with 50Hz
        #self.p.start(2.5) # Initialization
        self.p.start(0)
        
        self.starting_angle = None
        self.wait_time = None

    def set_angle(self, angle, block):
        print("angles",self.starting_angle,angle)
        if self.starting_angle != angle:
            norm = angle / 180.0
            norm = min(1,max(0,norm))
            self.p.ChangeDutyCycle(norm * 8.4 + 2.2)
            
            if self.starting_angle == None:
                delta = 180
            else:
                delta = abs(self.starting_angle - angle)
                
            if block:
                time.sleep(delta * 0.4 / 180 + 0.05)
                self.starting_angle = angle
                self.p.ChangeDutyCycle(0)
            else:
                self.wait_time = time.time() + (delta * 0.4 / 180 + 0.05)
                
    def chill_bro(self):
        if self.wait_time !=None:
            if time.time()>self.wait_time:
                print("chilling")
                self.wait_time = None
                self.p.ChangeDutyCycle(0)
    
    def freeze_angle(self):
        self.p.ChangeDutyCycle(0)

    def stop(self):
        self.p.stop()
        GPIO.cleanup()
