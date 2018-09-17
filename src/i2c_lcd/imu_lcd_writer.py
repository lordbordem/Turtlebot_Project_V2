#!/usr/bin/env python3

import rospy
import mraa_i2c_led as lcd
from std_msgs.msg import String

lcd = lcd.lcd()

def rxCallbackLine1(data1):
    rospy.loginfo(data1.data)
    lcd.display_string("                 ", 1);
    lcd.display_string(data1.data, 1)

def listener():
    rospy.init_node('i2cLcdListener')
    rospy.Subscriber('imu', String, rxCallbackLine1)
    rospy.spin()

if __name__ == '__main__':
    listener()