#!/usr/bin/env python3
import cv2
import rospy
import mraa_i2c_led as lcd

import time

from std_msgs.msg import String, Float64, Int8
from sensor_msgs.msg import Imu
from BenIdentifier.predict import *

lcd = lcd.lcd()

line1 = "start init 1"
line2 = "start inti 2"
imuline1 = "imu init 1"
imuline2 = "imu init 2"
benline1 = "ben init 1"
benline2 = "bun init 2"
looptimer = 0
lastpressed = 2


def lcdDisplayLoop(dataLine1, dataLine2):
    global looptimer
    if time.time() - looptimer >= 1:
        lcd.display_string("                 ", 1);
        lcd.display_string("                 ", 2);
        lcd.display_string(dataLine1, 1)
        lcd.display_string(dataLine2, 2)
        looptimer = time.time()

def rxCallbackLine1(data1):
    global line1
    rospy.loginfo(data1.data)
    line1 = data1.data

def rxCallbackLine2(data1):
    global line1
    global line2
    global imuline1
    global imuline2
    global benline1
    global benline2

    #rospy.loginfo(str(round(data1.linear_acceleration.x,2)))

    benline1 = "Ben Prediction"
    #benline2 = predictBen()
    benline2 = "notben"
    imuline2 = "imu test"
    imuline1 ="Test " + "X=" + str(round(data1.linear_acceleration.x,2))
    imuline2 = "Y=" + str(round(data1.linear_acceleration.y,2)) + " Z=" + str(round(data1.linear_acceleration.z,2))

def callback(data):
    global lastpressed
    lastpressed = data.data


def listener():
    global line1
    global line2
    global imuline1
    global imuline2
    global benline1
    global benline2
    global lastpressed
    rospy.init_node('i2cLcdListener', anonymous=True)
    rospy.Subscriber('/imu', Imu, rxCallbackLine2)
    rospy.Subscriber('/pushed', Int8, callback)
    #rospy.Subscriber('LCDLine1', String, rxCallbackLine1)
    line1 = "test"
    buttonval = int (lastpressed)
    # imuline1 = "test"
    # if(buttonval == 2):
    #     line1 = str(buttonval)
    #     line2 = imuline2
    # elif(buttonval == 4):
    #     line1 = benline1
    #     line2 = benline2
    # else:
    #     line1 = "Last pressed"
    #     line2 = str(lastpressed)

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
