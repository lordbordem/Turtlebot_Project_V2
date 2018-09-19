#!/usr/bin/env python

import rospy
import mraa_i2c_led as lcd
import time

from std_msgs.msg import String, Float64, Int8, UInt16
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from BenIdentifier.predict import *
from tf.transformations import euler_from_quaternion
#import tf

lcd = lcd.lcd()
BenLine1 = "Starting B"
BenLine2 = "Ben"
ImuLine1 = "Starting"
ImuLine2 = "IMU"
RpmLine1 = "Speed m/s"
RpmLine2 = "init"
looptimer = 0
lastpressed = 2
rpm = 0
lastt = 0
lasty = 0
lastx = 0

def lcdDisplayLoop(dataLine1, dataLine2, benLine1, benLine2, rpmline1, rpmline2, button):
    line1 = ""
    line2 = ""
    if(button == 4):
        line1 = dataLine1
        line2 = dataLine2
    elif(button == 2):
        line1 = rpmline1
        line2 = rpmline2
    else:
        line1 = benLine1
        line2 = benLine2

    global looptimer
    if time.time() - looptimer >= 0.001:
        lcd.display_string(line1 + "                ", 1)
        lcd.display_string(line2 + "                ", 2)
        looptimer = time.time()

def rxCallbackLine2(data1):
    global ImuLine1
    global ImuLine2
    global BenLine1
    global BenLine2
    x_value = "{:.2f}".format(round(data1.linear_acceleration.x,2))
    y_value = "{:.2f}".format(round(data1.linear_acceleration.y,2))
    z_value = "{:.2f}".format(round(data1.linear_acceleration.z,2))

    ImuLine1 ="Acc(m/s) " + "X=" + str(x_value)
    ImuLine2 = "Y=" + str(y_value) + " Z=" + str(z_value)
    BenLine1 = "Ben Finder"
    BenLine2 = predictBen()
    #BenLine2 = "test"
def callback(data):
    global lastpressed
    lastpressed = data.data

def callbackrpm(data):
    global RpmLine2
    #q = (data.pose.pose.orientation.x, 
    #     data.pose.pose.orientation.y, 
    #     data.pose.pose.orientation.z, 
    #     data.pose.pose.orientation.w)
    #angles = euler_from_quaternion(q)
    #RpmLine2 = "%.5f" % (angles[2])
    RpmLine2 = "%.5f" % data.twist.twist.linear.x



def listener():
    global ImuLine1
    global ImuLine2
    global BenLine1
    global BenLine2
    global lastpressed
    global RpmLine1
    global RpmLine2
    rospy.init_node('i2cLcdListener')
    rospy.Subscriber('/pushed', Int8, callback)
    rospy.Subscriber('/imu', Imu, rxCallbackLine2)
    rospy.Subscriber('/odom', Odometry, callbackrpm)


    while True:
        lcdDisplayLoop(ImuLine1, ImuLine2, BenLine1, BenLine2, RpmLine1, RpmLine2, lastpressed)
    rospy.spin()

if __name__ == '__main__':
    listener()




# global RpmLine2
# global lastx
# global lasty
# global lastt
# currentx = data.pose.pose.position.x
# currenty = data.pose.pose.position.y
# currentt = int (time.time())
# dx = currentx - lastx
# dy = currenty - lasty
# d = math.sqrt(dx * dx + dy * dy)
# dt = currentt - lastt
# speed = d / dt
#
# RpmLine2 = str(speed)
# lastx = currentx
# lasty = currenty
# lastt = currentt
