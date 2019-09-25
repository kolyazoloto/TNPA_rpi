#!/usr/bin/env python
import numpy as np
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Int64MultiArray
import pigpio


class PWM_Manip():

        def __init__(self):
		self.pi=pigpio.pi()                
                rospy.init_node("joyCameraManipulator_to_pwm", anonymous=True)
                rospy.Subscriber("/joy", Joy, self.callback)
                self.manipPub = rospy.Publisher("/manip",Int64MultiArray,queue_size=0)
		self.buttonX = 0
		self.buttonA = 0
		self.prevManipPub = [0,0]
		self.manipPWM = 1500
		self.manipPWMCleshni = 1500
	        self.cameraPWM = 1400
		rospy.on_shutdown(self.shutdown)
                rospy.spin()

	def shutdown(self):
		self.pi.set_servo_pulsewidth(17,0)
                self.pi.set_servo_pulsewidth(27,0)
		self.pi.set_servo_pulsewidth(22,0)

        def callback(self,data):
	       self.buttonX = data.buttons[2]
	       self.buttonA = data.buttons[3]
	       self.buttonY = data.buttons[0]
	       self.buttonB = data.buttons[1]
	       self.buttonUP = data.buttons[5]
	       self.buttonDOWN = data.buttons[4]

    	       if self.buttonDOWN == 1:
	          self.cameraPWM -= 50
		  if self.cameraPWM < 500:
		      self.cameraPWM = 500

    	       if self.buttonUP == 1:
	          self.cameraPWM += 50
		  if self.cameraPWM > 2500:
		      self.cameraPWM = 2500

    	       if self.buttonX == 1:
	          self.manipPWM -= 20
		  if self.manipPWM < 500:
		      self.manipPWM = 500

    	       if self.buttonA == 1:
	          self.manipPWM += 20
		  if self.manipPWM > 2500:
		      self.manipPWM = 2500

    	       if self.buttonY == 1:
	          self.manipPWMCleshni += 20
		  if self.manipPWMCleshni > 2500:
		      self.manipPWMCleshni = 2500

    	       if self.buttonB == 1:
	          self.manipPWMCleshni -= 20
		  if self.manipPWMCleshni < 500:
		      self.manipPWMCleshni = 500
	       intManipPub = [int(self.manipPWM),int(self.manipPWMCleshni),int(self.cameraPWM)]
	       if intManipPub != self.prevManipPub:
		   print(intManipPub)
                   self.manipPub.publish(data=intManipPub)

		   self.pi.set_servo_pulsewidth(17,int(self.manipPWM))
                   self.pi.set_servo_pulsewidth(27,int(self.manipPWMCleshni))
		   self.pi.set_servo_pulsewidth(22,int(self.cameraPWM))
	       self.prevManipPub = intManipPub 




	       
               
try:       
        manip = PWM_Manip()
except rospy.ROSInterruptException:
        pass

                        

		
         
