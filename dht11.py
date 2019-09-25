#!/usr/bin/python
import Adafruit_DHT,rospy
from std_msgs.msg import Float64
import time

def publisher():
    sensor = Adafruit_DHT.DHT22
    pin = 18
    rospy.init_node("dht11",anonymous=True)
    rate = rospy.Rate(1)
    pub_humidity = rospy.Publisher("/dht11",Float64,queue_size=0)
    while not rospy.is_shutdown():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            #print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
	    pub_humidity.publish(data = humidity)
	    #print(humidity)
        else:
            print('Failed to get rrosrun eading. Try again!')
	    rate.sleep()
	

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
