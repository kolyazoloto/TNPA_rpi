#!/usr/bin/python
import ms5837,rospy
from std_msgs.msg import Float64,Bool
import time

global depthKoef,depth
depthKoef = 0

def callback(data):
    global depthKoef,depth
    depthKoef = depth
def publisher():
    global depthKoef,depth
    sensor = ms5837.MS5837_30BA()
    if not sensor.init():
        print "Sensor could not be initialized"
        exit(1)
    rospy.init_node("ms5837",anonymous=True)
    pub_bar = rospy.Publisher("/ms5837/pressure",Float64,queue_size=0)
    pub_temp = rospy.Publisher("/ms5837/temp",Float64,queue_size=0)
    rospy.Subscriber("/interface/depthKoef",Bool,callback)
    while not rospy.is_shutdown():
        if sensor.read():
	    depth = sensor.depth()
	    depthKoef = depth - depthKoef
	    temp = sensor.temperature()
	    pub_bar.publish(data = depthKoef)
	    pub_temp.publish(data = temp)
        else:
            print "Sensor read failed!"


if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
