#!/usr/bin/env python

import pigpio
import time

class Servo:
    def __init__(self, pin, pi):
        self.pin = pin
        self.pi = pi

        self.pi.hardware_PWM(13,50,40_000)
        
        self.starting_angle = None
        self.wait_time = None

    def set_angle(self, angle, block):
        print("angles",self.starting_angle,angle,"pin",self.pin)
        if self.starting_angle != angle:
            norm = angle / 180.0
            norm = min(1,max(0,norm))
            print("value",int((norm * 8.4 + 2.2)*10_000))
            self.pi.hardware_PWM(self.pin,50,int((norm * 8.4 + 2.2)*10_000))            
            if self.starting_angle == None:
                delta = 180
            else:
                delta = abs(self.starting_angle - angle)
                
            self.starting_angle = angle            
            if block:
                time.sleep(delta * 0.5 / 180 + 0.1)
                
                self.pi.hardware_PWM(self.pin,50,0)
            else:
                self.wait_time = time.time() + (delta * 0.4 / 180 + 0.05)
                
    def chill_bro(self):
        if self.wait_time !=None:
            if time.time()>self.wait_time:
                print("chilling")
                self.wait_time = None
                self.pi.hardware_PWM(self.pin,50,0)
    
    def freeze_angle(self):
        self.pi.hardware_PWM(self.pin,50,0)

    def stop(self):
        pass
        #self.p.stop()
