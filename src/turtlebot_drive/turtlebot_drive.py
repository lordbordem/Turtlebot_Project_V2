#!/usr/bin/env python

import math
import rospy
import std_msgs.msg as stdMessage
import sensor_msgs.msg as sensorMessage
import geometry_msgs.msg as geoMessage
import nav_msgs.msg as navigationMessage
from tf.transformations import euler_from_quaternion
from tf.msg import tfMessage
#from tf.transformations import euler_from_quaternion
LaserDistance = 0
OdomData = 0
currentAngle = 0
driveData = 0
driveController = 0
musicController = 0
startTurn = False
rosRxFirst = False
firstTurn = False
startAngle = 0
debugState = 0
drivePause = 0
buttonState = 3
driveStop = False

def LaserCallback(data):
    global LaserDistance
    global debugState
    global rosRxFirst
    if debugState == 0 and data.ranges[0] != 0:
        LaserDistance = data.ranges[0]
    elif debugState == 1 and data.ranges[180] != 0:
        LaserDistance = data.ranges[180]
    rosRxFirst = True
#hi
def OdomCallback(data):
    global OdomData
    global currentAngle
    OdomData = data
    quat = (data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w) 
    eul = euler_from_quaternion(quat)
    currentAngle = math.degrees(eul[2]) 
    #rospy.loginfo(currentAngle)
    pass

def debugCallback(data):
    global debugState
    debugState = data.data
    pass

def buttonCallback(data):
    global buttonState
    if data.data == 3 or data.data == 1:
        buttonState = data.data
    rospy.loginfo(buttonState)

def turnRightAngleUpdate():
    global driveController
    global driveData
    global startTurn

    driveData = geoMessage.Twist()

    if startTurn == True:
        AngleOffset = abs((startAngle + 180) - (currentAngle + 180))
        if AngleOffset < 90:
            driveData.angular.z = 0.2
            driveData.linear.x = 0
        else:
            startTurn = False
    else:
        driveData.angular.z = 0
        driveData.linear.x = 0.2

def readLDSBool():
    global startTurn
    global LaserDistance
    global firstTurn
    global driveStop
    if LaserDistance <= 0.4 and LaserDistance != 0 and startTurn == False and firstTurn == False:
        startAngle = currentAngle
        musicController.publish(1)
        startTurn = True
        firstTurn = True
    elif LaserDistance <= 0.4 and LaserDistance != 0 and startTurn == False and firstTurn == True:
        musicController.publish(2)
        driveStop = True


def shutdownProcedure():
    global driveController
    global driveData
    global musicController
    global drivePause
    driveController = rospy.Publisher('/cmd_vel',geoMessage.Twist, queue_size=1)
    driveData = geoMessage.Twist()
    driveData.angular.z = 0
    driveData.linear.x = 0
    driveController.publish(driveData)


if __name__ == '__main__':
    global driveData
    global drivePause
    global buttonState
    global driveStop
    driveData = geoMessage.Twist()
    rospy.init_node('turtlebot_drive')
    rospy.on_shutdown(shutdownProcedure)
    rospy.Subscriber('/scan', sensorMessage.LaserScan, LaserCallback)
    rospy.Subscriber('/odom', navigationMessage.Odometry, OdomCallback)
    rospy.Subscriber('/mx2Diag', stdMessage.Int32, debugCallback)
    rospy.Subscriber('/pushed', stdMessage.Int8, buttonCallback)
    driveController = rospy.Publisher('/cmd_vel',geoMessage.Twist, queue_size=1)
    musicController = rospy.Publisher('/play_melody',stdMessage.Int8, queue_size=1)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if buttonState == 1 and driveStop == False:
            readLDSBool()
            turnRightAngleUpdate()
        else: 
            driveData.angular.z = 0
            driveData.linear.x = 0
        driveController.publish(driveData)
        rate.sleep()
    
    rospy.spin()
#