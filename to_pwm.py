#!/usr/bin/env python
import numpy as np
import rospy
from geometry_msgs.msg import Twist
import time
import pigpio


class PWM_Manip():
        def __init__(self):                
               self.pi=pigpio.pi()
               rospy.init_node("ManipNode", anonymous=True)
               rospy.Subscriber("mux_topic",Twist, self.callback)
	       #self.initDriver()
               rospy.spin()
                
        def callback(self,data):               
               y = data.linear.x  # vpered nazad
               x = data.angular.z # levo pravo
	       z = data.linear.z  # vpered nazad
	       #x = data.axes[0]
	       #y =data.axes[1] 
               dutycycle = [y,y,z]
               if x > 0:
                       dutycycle[0] *= 1 - np.abs(x) #centr 1  bok 0
               if x < 0:
                       dutycycle[1] *= 1 - np.abs(x)
               #####################
	       dutycycle[0]  = (dutycycle[0]*500) + 1500
	       dutycycle[1]  = (dutycycle[1]*500) + 1500
	       dutycycle[2]  = (dutycycle[2]*500) + 1500
	       #####################
               self.pi.set_servo_pulsewidth(25,dutycycle[0])
	       self.pi.set_servo_pulsewidth(11,dutycycle[0])

               self.pi.set_servo_pulsewidth(23,dutycycle[1])
	       self.pi.set_servo_pulsewidth(9,dutycycle[1])

	       self.pi.set_servo_pulsewidth(24,dutycycle[2])
	       self.pi.set_servo_pulsewidth(10,dutycycle[2])

	        
               rospy.loginfo(dutycycle) 

 	def initDriver(self):
		dutycycle = 1500
		while dutycycle != 2000:
			dutycycle +=10
			time.sleep(0.01)
			self.pi.set_servo_pulsewidth(23,dutycycle)
			self.pi.set_servo_pulsewidth(9,dutycycle)

               		self.pi.set_servo_pulsewidth(24,dutycycle)
			self.pi.set_servo_pulsewidth(10,dutycycle)

			self.pi.set_servo_pulsewidth(25,dutycycle) 
			self.pi.set_servo_pulsewidth(11,dutycycle) 
			print(dutycycle)
		time.sleep(0.2)
		while dutycycle != 1000:
			dutycycle -=10
			time.sleep(0.01)
			self.pi.set_servo_pulsewidth(23,dutycycle)
			self.pi.set_servo_pulsewidth(9,dutycycle)

               		self.pi.set_servo_pulsewidth(24,dutycycle)
			self.pi.set_servo_pulsewidth(10,dutycycle)

			self.pi.set_servo_pulsewidth(25,dutycycle) 
			self.pi.set_servo_pulsewidth(11,dutycycle) 
			print(dutycycle)
		time.sleep(0.2)
		while dutycycle != 1500:
			dutycycle +=10
			time.sleep(0.005)
			self.pi.set_servo_pulsewidth(23,dutycycle)
			self.pi.set_servo_pulsewidth(9,dutycycle)

               		self.pi.set_servo_pulsewidth(24,dutycycle)
			self.pi.set_servo_pulsewidth(10,dutycycle)

			self.pi.set_servo_pulsewidth(25,dutycycle) 
			self.pi.set_servo_pulsewidth(11,dutycycle) 
			print(dutycycle)
			
        def shutdown(self):
	       self.pi.set_servo_pulsewidth(23,0)
	       self.pi.set_servo_pulsewidth(9,0)
	       self.pi.set_servo_pulsewidth(24,0)
	       self.pi.set_servo_pulsewidth(10,0)
	       self.pi.set_servo_pulsewidth(25,0)
               self.pi.set_servo_pulsewidth(11,0)
               self.pi.stop()      
    

try:       
        manip = PWM_Manip()
        rospy.on_shutdown(manip.shutdown)
except rospy.ROSInterruptException:
        pass

                        

		
        
