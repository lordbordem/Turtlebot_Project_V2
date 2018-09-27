#!/usr/bin/env python

import math
import rospy
import std_msgs.msg as stdMessage
import sensor_msgs.msg as sensorMessage
import geometry_msgs.msg as geoMessage
import nav_msgs.msg as navigationMessage
from tf.transformations import euler_from_quaternion
from tf.msg import tfMessage


class turtlebot_drive(object):
    def __init__(self):
        self.driveData = 0
        self.driveController = 0
        self.rosRxFirst = False
        self.startTurn = False
        self.rosRxFirst = False
        self.firstTurn = False
        self.startAngle = 0
        self.currentAngle = 0
        self.endAngle = 0
        self.debugState = 0
        self.drivePause = 0
        self.driveStop = False
        self.startTurn = False
        self.TurnsComplete = 0
        self.odomData = None
        self.maxSpeed = 0.26 #Turtlebot3 Waffle Max Speed
        self.Kp = 0.8 # Turtlebot3 Tuned Error Rate
        self.quaternion = None
        self.euler = None
        self.LaserDistance = None
        self.buttonState = 0
        self.debugState = 0
        self.botTwistDriver = geoMessage.Twist()
        self.velocityPublisher = rospy.Publisher('/cmd_vel', geoMessage.Twist, queue_size=1)
        self.odomSubscriber = rospy.Subscriber('/odom', navigationMessage.Odometry, self.OdomCallback)
        self.laserSubscriber = rospy.Subscriber('/scan', sensorMessage.LaserScan, self.LaserCallback)
        self.debugSubscriber = rospy.Subscriber('/mx2Diag', stdMessage.Int32, self.debugCallback)
        self.buttonSubscriber = rospy.Subscriber('/pushed', stdMessage.Int8, self.buttonCallback)

    def LaserCallback(self, data):
        if self.debugState is 0 and data.ranges[0] is not 0:
            self.LaserDistance = data.ranges[0]
        elif self.debugState is 1 and data.ranges[180] is not 0:
            self.LaserDistance = data.ranges[180]
        self.rosRxFirst = True

    def OdomCallback(self, data):
        self.odomData = data
        self.quaternion = (data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w)
        self.euler = euler_from_quaternion(self.quaternion)
        self.currentAngle = math.degrees(self.euler[2])
        #rospy.loginfo(currentAngle)
        pass

    def debugCallback(self, data):
        self.debugState = data.data
        pass

    def buttonCallback(self, data):
        if data.data == 3 or data.data == 1:
            self.buttonState = data.data
        rospy.loginfo(self.buttonState)

    def turn(self, angle):
        angular_turn = (self.Kp * angle)

        if angular_turn > 0:
            angular_turn = self.maxSpeed
        else:
            angular_turn = -self.maxSpeed

        self.botTwistDriver.linear.x = 0
        self.botTwistDriver.linear.y = 0
        self.botTwistDriver.linear.z = 0
        self.botTwistDriver.angular.x = 0
        self.botTwistDriver.angular.y = 0
        self.botTwistDriver.angular.z = -angular_turn
        self.TurnsComplete += 1
        self.velocityPublisher.publish(self.botTwistDriver)

    def goStraight(self):
        self.botTwistDriver.linear.x = self.maxSpeed
        self.botTwistDriver.linear.y = 0
        self.botTwistDriver.linear.z = 0
        self.botTwistDriver.angular.x = 0
        self.botTwistDriver.angular.y = 0
        self.botTwistDriver.angular.z = 0
        self.velocityPublisher.publish(self.botTwistDriver)

    def allStop(self):
        self.botTwistDriver.linear.x = 0
        self.botTwistDriver.linear.y = 0
        self.botTwistDriver.linear.z = 0
        self.botTwistDriver.angular.x = 0
        self.botTwistDriver.angular.y = 0
        self.botTwistDriver.angular.z = 0
        self.driveStop = True
        self.velocityPublisher.publish(self.botTwistDriver)

    def getButtonState(self):
        return self.buttonState

    def getDriveStopState(self):
        return self.driveStop

    def getLaserDistance(self):
        return self.LaserDistance

    def getCurrentAngle(self):
        return self.currentAngle

    def getStartTurn(self):
        return self.startTurn

    def getTurnsComplete(self):
        return self.TurnsComplete

    def getStartAngle(self):
        return self.startAngle

    def setStartAngle(self, angle):
        self.startAngle = angle

    def setEndAngle(self, angle):
        self.endAngle = angle

    def setStartTurn(self, start):
        self.startTurn = start


def turnRightAngleUpdate(bot_driver):
    startTurn = bot_driver.getStartTurn()
    startAngle = bot_driver.getStartAngle()
    currentAngle = bot_driver.getCurrentAngle()

    if startTurn is True:
        AngleOffset = abs((startAngle + 180) - (currentAngle + 180))
        if AngleOffset < 90:
            bot_driver.turn(angle=AngleOffset)
        else:
            bot_driver.setStartTurn(start=False)
    else:
        bot_driver.goStraight()


def readLDSBool(bot_driver):

    LaserDistance = bot_driver.getLaserDistance()
    musicController = rospy.Publisher('/play_melody', stdMessage.Int8, queue_size=1)
    startTurn = bot_driver.getStartTurn()
    TurnsComplete = bot_driver.getTurnsComplete()

    if LaserDistance <= 0.4 and LaserDistance != 0 and startTurn is False and TurnsComplete is 0:
        bot_driver.setStartAngle(bot_driver.getCurrentAngle())
        musicController.publish(1)
        bot_driver.setStartTurn(start=True)
    elif LaserDistance <= 0.4 and LaserDistance != 0 and startTurn is False and TurnsComplete > 0:
        musicController.publish(2)
        bot_driver.allStop()


def shutdown_ros(bot_driver):
    bot_driver.allStop()


def run_assignment3():
    bot_driver = turtlebot_drive()

    rospy.init_node('turtlebot_drive')
    rospy.on_shutdown(shutdown_ros(bot_driver))
    updateRate = rospy.Rate(10)

    while not rospy.is_shutdown():
        if bot_driver.getButtonState() is 1 and bot_driver.getDriveStopState() is False:
            readLDSBool(bot_driver)
            turnRightAngleUpdate(bot_driver)

        else:
            bot_driver.allStop()

        updateRate.sleep()
    rospy.spin()


if __name__ == '__main__':
    try:
        run_assignment3()
    except rospy.ROSInterruptException:
        pass
