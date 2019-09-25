#!/usr/bin/env python
import numpy as np
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist 
import dynamic_reconfigure.client


class PWM_Manip():
        def __init__(self):                
            rospy.init_node("control_effort_to_twist", anonymous=True)
            rospy.Subscriber("/control_effort", Float64, self.callbackServo)
            rospy.Subscriber("/interface/motor_slider", Float64, self.callbackMotor)
            self.x = 0
            self.y = 0
            self.run = False
            self.reverse = False
            self.twist = Twist()
            self.twistPub = rospy.Publisher("/autocourse_twist",Twist,queue_size=0)

            rospy.spin()
        def callbackServo(self,data):                
            self.x = data.data/100 
            self.twist.angular.z = -self.x  ######
            self.twist.linear.x = self.y

            self.twistPub.publish(self.twist)
        def callbackMotor(self,data):
            if self.reverse == True:
                data.data = -data.data
                
            self.y = data.data/100
            if self.run == 1:
                self.twist.angular.z = -self.x ##########
                self.twist.linear.x = self.y       
            if self.run == 0:
                self.twist.angular.z = 0
                self.twist.linear.x = 0
            self.twistPub.publish(self.twist)
try:       
        manip = PWM_Manip()
except rospy.ROSInterruptException:
        pass



		
         
