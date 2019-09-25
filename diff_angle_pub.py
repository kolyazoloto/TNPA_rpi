#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import Imu, MagneticField
from std_msgs.msg import Header, Float64, Float64MultiArray, Int64
from tf.transformations import euler_from_quaternion

bool_first = 0
global last_published,course
last_published = 0
course = 0


def function():
    rospy.init_node("delta_angle_publisher",anonymous=True)
    global pub_angle
    pub_angle = rospy.Publisher("/imu/delta_angle",Float64,queue_size=0)
    rospy.Subscriber("imu/data",Imu,callback)
    rospy.Subscriber("interface/course_to",Float64,courseCallback)
    rospy.spin()

def courseCallback(data):
    global course
    course = data.data

def callback(data):
    global bool_first,porog_queue,pub_angle,last_published,course
    quat_list = [data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w]
    euler = euler_from_quaternion(quat_list)
    az = euler[-1]
    az = az*180/np.pi
    if az > 180:
        az -= 360
    delta_angle = course - az
    rospy.loginfo(delta_angle)
    #doljno ubrat' perehod cherez nol'
    if delta_angle > 180:
        delta_angle -=360
    if delta_angle < -180:
        delta_angle +=360
    ### koroche esli raznie soobsheniya to otpravlyaet
    if bool_first == 0:    #otpravlyaem pervoe soobshenie vsegda        
        pub_angle.publish(delta_angle)
        last_published = delta_angle
        bool_first = 1
    else:
        if abs(delta_angle-last_published) > 0:  #na skolko gradusov zamechaem
            pub_angle.publish(delta_angle)
            last_published = delta_angle
       
try:
    function()
except rospy.ROSInterruptException:
    pass
