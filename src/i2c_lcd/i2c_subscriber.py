#!/usr/bin/env python3

import rospy
import mraa_i2c_led as lcd

import time

from std_msgs.msg import String, Float64
from sensor_msgs.msg import Imu

lcd = lcd.lcd()

line1 = "h"
line2 = ""
looptimer = 0

def lcdDisplayLoop(dataLine1, dataLine2):
    global looptimer
    if time.time() - looptimer >= 0.001:
        #lcd.display_string("                 ", 1);
        #lcd.display_string("                 ", 2);
        #lcd.clear()
        lcd.display_string(dataLine1 + "                ", 1)
        lcd.display_string(dataLine2 + "                ", 2)
        looptimer = time.time()

def rxCallbackLine1(data1):
    global line1
    rospy.loginfo(data1.data)
    line1 = data1.data

def rxCallbackLine2(data1):
    global line2
    global line1
    #rospy.loginfo(str(round(data1.linear_acceleration.x,2)))
    line1 ="Acc(m/s) " + "X=" + "{:.2f}".format(round(data1.linear_acceleration.x,2)) 
    y_value = "{:.2f}".format(round(data1.linear_acceleration.y,2))
    z_value = "{:.2f}".format(round(data1.linear_acceleration.z,2))
    line2 = "Y=" + str(y_value) + " Z=" + str(z_value)

def listener():
    global line1
    global line2
    rospy.init_node('i2cLcdListener')
    #rospy.Subscriber('LCDLine1', String, rxCallbackLine1)
    rospy.Subscriber('/imu', Imu, rxCallbackLine2)
    try:
        while True:
            try:
                lcdDisplayLoop(line1, line2)
            except KeyboardInterrupt:
                exit()
    except:
        exit()
    rospy.spin()

if __name__ == '__main__':
    listener()