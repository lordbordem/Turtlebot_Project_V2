#!/usr/bin/env python

import rospy
import std_msgs.msg as stdMessage
import sensor_msgs.msg as sensorMessage
import geometry_msgs.msg as geoMessage
import nav_msgs.msg as navigationMessage
#from tf.msg import tfMessage
#from tf.transformations import euler_from_quaternion
LaserDistance = 0
OdomData = 0
currentAngle = 0
driveData = 0
driveController = 0
startTurn = 0
startAngle = 0
driveSpee = 0
def LaserCallback(data):
    global LaserDistance
    LaserDistance = data.ranges[0]
    pass

def OdomCallback(data):
    global OdomData
    quat = data.pose.pose.orientation
    #currentAngle
    pass

def turnRightAngleUpdate():
    global driveController
    global driveData
    global startTurn
    driveData = geoMessage.Twist()
    if LaserDistance <= 0.4: #startTurn == True:
        # if (startAngle+90) - currentAngle < 90:
        #     driveData.angular.z = 100
        #     driveData.linear.x = 0
        # else:
        #     startTurn = False
        driveData.angular.z = 0
        driveData.linear.x = 0
    else:
        driveData.angular.z = 0
        driveData.linear.x = 0.2

def readLDSBool():
    global startTurn
    if LaserDistance <= 0.4:# and startTurn == False:
        startTurn = True


if __name__ == '__main__':
    rospy.init_node('turtlebot_drive')
    rospy.Subscriber('/scan', sensorMessage.LaserScan, LaserCallback)
    rospy.Subscriber('/odom', navigationMessage.Odometry, OdomCallback)
    driveController = rospy.Publisher('/cmd_vel',geoMessage.Twist, queue_size=1)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        #readLDSBool()
        turnRightAngleUpdate()
        driveController.publish(driveData)
        rate.sleep()
    driveData.angular.z = 0
    driveData.linear.x = 0
    driveController.publish(driveData)
    rospy.spin()
