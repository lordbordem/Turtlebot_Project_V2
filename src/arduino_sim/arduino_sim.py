#!/usr/bin/env python

import rospy

from std_msgs.msg import String, Float64, Int8, UInt16
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from sensor_msgs.msg import Image
import interface
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError


class sim_module(object):
    def __init__(self):
        self.lcd = None
        self.num_lcd_rows = 2
        self.ben_line = ["Starting", "Ben"]
        self.imu_line = ["Starting", "IMU"]
        self.rpm_line = ["Starting", "Speed m/s"]
        self.loop_timer = 0
        self.last_button_pressed = 2
        self.rpm = 0
        self.timer_interval = 0.001
        self.current_menu = 0
        self.last_string_length = 0
        self.ben_identifier = None
        self.cv_depth_image = None
        self.cv_rgb_image = None
        self.rgb_get = False
        self.depth_get = False

        self.text_xpos = 1050
        self.text_ypos = 350
        self.text_pos_multiplier = 40
        self.font_size = 30

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.rgbCallback)
        self.depth_sub = rospy.Subscriber("/camera/depth/image_raw", Image, self.depthCallback)

        self.imu_values = rospy.Subscriber('/imu', Imu, self.imuCallback)
        self.odom_values = rospy.Subscriber('/odom', Odometry, self.rpmCallback)

        self.music_subscriber = rospy.Subscriber('/play_melody', Int8, self.musicCallback)
        self.button_publisher = rospy.Publisher('/pushed', Int8, queue_size=1)

        self.main_interface = interface.interface()

    def init_sim(self):
        self.main_interface.start_screen()
        self.main_interface.init_joystick()
        #self.main_interface.create_menu()
        self.display_text(("Starting", "MX2"))

    def display_text(self, line):
        for i, text in enumerate(line):
            self.main_interface.display_text(text, self.text_xpos, (self.text_ypos + (self.text_pos_multiplier*i)), self.font_size)

    def update_current_menu(self, menu):
        self.current_menu = menu

    def update_frame(self):
        if self.rgb_get is True:
            self.menu_loop()
            self.main_interface.update_frame(self.cv_rgb_image)
            self.rgb_get = False

        self.main_interface.process_events()


        # if self.depth_get is True and self.rgb_get is True:
        #     self.cv_depth_image = cv2.cvtColor(self.cv_depth_image, cv2.COLOR_GRAY2BGR)
        #     display = np.vstack((self.cv_rgb_image, self.cv_depth_image))
        #     self.menu_loop()
        #     self.main_interface.update_frame(display)
        #     self.depth_get = False
        #     self.rgb_get = False
        #
        # self.main_interface.process_events()

    def menu_loop(self):
        self.last_button_pressed = self.main_interface.get_key_input()
        self.button_publisher.publish(self.last_button_pressed)
        if(self.last_button_pressed is 4):
            self.display_text(self.imu_line)

        elif(self.last_button_pressed == 2):
            self.display_text(self.rpm_line)

        elif(self.last_button_pressed == 0):
            self.display_text(self.ben_line)

    def imuCallback(self, data):
        x_value = "{:.2f}".format(round(data.linear_acceleration.x, 2))
        y_value = "{:.2f}".format(round(data.linear_acceleration.y, 2))
        z_value = "{:.2f}".format(round(data.linear_acceleration.z, 2))

        self.imu_line[0] = "Acc(m/s) " + "X=" + str(x_value)
        self.imu_line[1] = "Y=" + str(y_value) + " Z=" + str(z_value)

    def rpmCallback(self, data):
        # q = (data.pose.pose.orientation.x,
        #     data.pose.pose.orientation.y,
        #     data.pose.pose.orientation.z,
        #     data.pose.pose.orientation.w)
        # angles = euler_from_quaternion(q)
        # RpmLine2 = "%.5f" % (angles[2])
        self.rpm_line[0] = "Speed m/s"
        self.rpm_line[1] = "%.5f" % data.twist.twist.linear.x

    def musicCallback(self, data):
        # q = (data.pose.pose.orientation.x,
        #     data.pose.pose.orientation.y,
        #     data.pose.pose.orientation.z,
        #     data.pose.pose.orientation.w)
        # angles = euler_from_quaternion(q)
        # RpmLine2 = "%.5f" % (angles[2])
        text = "Music: No " + str(data)
        self.main_interface.display_text(text, self.text_xpos, (self.text_ypos + (self.text_pos_multiplier*4)), self.font_size)

    def get_cv_rgb_image(self):
        return self.cv_rgb_image

    def get_cv_depth_image(self):
        return self.cv_depth_image

    def rgbCallback(self, data):
        try:
            self.cv_rgb_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.rgb_get = True
        except CvBridgeError as e:
            print(e)

    def depthCallback(self, data):
        try:
            self.cv_depth_image = self.bridge.imgmsg_to_cv2(data)
            self.depth_get = True
        except CvBridgeError as e:
            print(e)


def listener():

    menu = sim_module()
    menu.init_sim()
    rospy.init_node('arduino_sim')

    rate = rospy.Rate(60)  # 60hz

    while not rospy.is_shutdown():
        menu.update_frame()
        rate.sleep()

    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
