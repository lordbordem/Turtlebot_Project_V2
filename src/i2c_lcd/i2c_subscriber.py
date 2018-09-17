#!/usr/bin/env python3

import rospy
import mraa_i2c_led as lcd

import time

from std_msgs.msg import String, Float64
from sensor_msgs.msg import Imu

lcd = lcd.lcd()

ImuLine1 = "Starting"
ImuLine2 = ""
looptimer = 0

def lcdDisplayLoop(dataLine1, dataLine2):
    global looptimer
    if time.time() - looptimer >= 0.001:
        lcd.display_string(dataLine1 + "                ", 1)
        lcd.display_string(dataLine2 + "                ", 2)
        looptimer = time.time()

def rxCallbackLine2(data1):
    global ImuLine1
    global ImuLine2
    
    x_value = "{:.2f}".format(round(data1.linear_acceleration.x,2))
    y_value = "{:.2f}".format(round(data1.linear_acceleration.y,2))
    z_value = "{:.2f}".format(round(data1.linear_acceleration.z,2))

    ImuLine1 ="Acc(m/s) " + "X=" + str(x_value)
    ImuLine2 = "Y=" + str(y_value) + " Z=" + str(z_value)

def listener():
    global ImuLine1
    global ImuLine2
    rospy.init_node('i2cLcdListener')

    rospy.Subscriber('/imu', Imu, rxCallbackLine2)
    while True:
        lcdDisplayLoop(ImuLine1, ImuLine2)
    rospy.spin()

if __name__ == '__main__':
    listener()