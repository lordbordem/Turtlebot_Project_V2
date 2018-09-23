#!/usr/bin/env python

import rospy
import mraa_i2c_led as lcd

from std_msgs.msg import String, Float64, Int8, UInt16
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
import BenIdentifier.predict
from tf.transformations import euler_from_quaternion


class lcd_menu(object):
    def __init__(self):
        self.lcd = None
        self.num_lcd_rows = 2
        self.ben_line[self.num_lcd_rows] = ("Starting", "Ben")
        self.imu_line[self.num_lcd_rows] = ("Starting", "IMU")
        self.rpm_line[self.num_lcd_rows] = ("Starting", "Speed m/s")
        self.loop_timer = 0
        self.last_button_pressed = 2
        self.rpm = 0
        self.timer_interval = 0.001
        self.current_menu = 0
        self.last_string_length[self.num_lcd_rows] = 0
        self.ben_identifier = None

    def init_lcd(self):
        self.lcd = lcd.lcd()
        self.lcd.write_cmd(self.lcd.LCD_CURSOROFF)
        self.lcd.write_cmd(self.lcd.LCD_BLINKOFF)
        self.display_text(("Starting", "MX2"))

    def init_ben(self):
        self.ben_identifier = BenIdentifier.predict.ben_identifier(camera=0,
                                                                   liveTest=False,
                                                                   enable_realsense=False)
        self.ben_identifier.init_camera()

    def display_text(self, line):
        for i, text in enumerate(line):
            if len(text) > self.last_string_length[i]:
                self.lcd.clear()
            self.last_string_length[i] = len(text)

        for i, text in enumerate(line):
            self.lcd.display_string(text, i)

    def update_current_menu(self, menu):
        self.current_menu = menu

    def menu_loop(self):
        if(self.last_button_pressed == 4):
            self.display_text(self.imu_line)

        elif(self.last_button_pressed == 2):
            self.display_text(self.rpm_line)

        elif(self.last_button_pressed == 0):
            self.display_text(self.ben_line)

    def imuCallback(self, data):
        x_value = "{:.2f}".format(round(data.linear_acceleration.x, 2))
        y_value = "{:.2f}".format(round(data.linear_acceleration.y, 2))
        z_value = "{:.2f}".format(round(data.linear_acceleration.z, 2))

        self.imu_line[1] = "Acc(m/s) " + "X=" + str(x_value)
        self.imu_line[2] = "Y=" + str(y_value) + " Z=" + str(z_value)

    def buttonCallback(self, data):
        self.last_button_pressed = data.data

    def rpmCallback(self, data):
        # q = (data.pose.pose.orientation.x,
        #     data.pose.pose.orientation.y,
        #     data.pose.pose.orientation.z,
        #     data.pose.pose.orientation.w)
        # angles = euler_from_quaternion(q)
        # RpmLine2 = "%.5f" % (angles[2])
        self.rpm_line[1] = "Speed m/s"
        self.rpm_line[2] = "%.5f" % data.twist.twist.linear.x

    def ben_finder(self):
        self.ben_line[1] = "Ben Finder"
        ben_result = self.ben_identifier.predictBen()

        if ben_result is "ben":
            self.ben_line[2] = "Found Ben"
        else:
            self.ben_line[2] = "No Ben"


def listener():

    menu = lcd_menu()
    menu.init_ben()

    rospy.init_node('i2cLcdListener')
    rospy.Subscriber('/pushed', Int8, menu.buttonCallback)
    rospy.Subscriber('/imu', Imu, menu.imuCallback)
    rospy.Subscriber('/odom', Odometry, menu.rpmCallback)

    rate = rospy.Rate(60)  # 60hz

    while not rospy.is_shutdown():
        menu.menu_loop()
        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    listener()
