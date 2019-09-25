#!/usr/bin/env python
import numpy as np
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class PWM_Manip():
        def __init__(self):                
                rospy.init_node("joy_to_pwm", anonymous=True)
                rospy.Subscriber("/joy", Joy, self.callback)
                self.twistPub = rospy.Publisher("/manual_twist",Twist,queue_size=0)
                self.run = 0
		self.manipulatorPWM = 0
                rospy.spin()

        def callback(self,data):
               y = data.axes[1]
               x = -data.axes[3]
	       self.buttonX = data.buttons[2]
	       self.buttonA = data.buttons[0]
               vniz = ((data.axes[2] + 1) / 2) -1  # ot 0 do -1
               vverh = (((data.axes[5] + 1) / 2) - 1) * (-1) # ot 0 do 1
               z = vverh + vniz 
               twist = Twist()
               #if run_param == True:
               twist.angular.z = x ## levo pravo
               twist.linear.x = y # vpered nazad
               twist.linear.z = z  # vverh vniz
               '''else:
                   twist.angular.z = 0
                   twist.linear.x = 0 '''
               print(twist)
               self.twistPub.publish(twist)
try:       
        manip = PWM_Manip()
except rospy.ROSInterruptException:
        pass

                        

		
         
