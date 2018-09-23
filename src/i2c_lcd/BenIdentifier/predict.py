import BenIdentifier.helper
import os
import csv
import scipy
from scipy import ndimage
import pickle
import cv2
import sys
import rospy
import pyrealsense2 as rs
import numpy as np


class ben_identifier(object):

    def __init__(self, camera=0, enable_realsense=False, liveTest=False):
        self.num_px = 64
        self.my_label_y = [1]
        self.liveTest = liveTest
        self.parameters = pickle.load(open("/home/turtlebot/catkin_ws/src/i2c_lcd/BenIdentifier/weights.p", "rb"))
        (self.train_x_orig,
         self.train_y,
         self.test_x_orig,
         self.test_y,
         self.classes) = BenIdentifier.helper.load_data()
        self.count = 0
        self.height = 480
        self.width = 680
        self.camera_num = camera
        self.camera = None
        self.work_image = None
        self.work_depth_image = None
        self.enable_realsense = enable_realsense
        self.rs_pipeline = None
        self.rs_config = None
        self.rs_framerate = 30
        self.color_image = None
        self.depth_image = None
        self.rs_frames = None

    def init_camera(self):
        if self.enable_realsense is not True:
            try:
                self.camera = cv2.VideoCapture(self.camera_num)
            except cv2.error as e:
                print("OpenCV Error", e)
                sys.exit(1)
        else:
            self.rs_pipeline = rs.pipeline()
            self.rs_config = rs.config()
            self.rs_config.enable_stream(rs.stream.depth, self.width,
                                         self.height, rs.format.z16,
                                         self.rs_framerate)
            self.rs_config.enable_stream(rs.stream.color, self.width,
                                         self.height,
                                         rs.format.bgr8,
                                         self.rs_framerate)
            self.rs_pipeline.start(self.rs_config)

    def grab_frame(self):
        if self.enable_realsense is not True:
            try:
                self.work_image = self.camera.read()
            except cv2.error as e:
                print("OpenCV Error", e)
                sys.exit(1)
        else:
            self.rs_frames = self.rs_pipeline.wait_for_frames()
            self.depth_image = self.rs_frames.get_depth_frame()
            self.color_image = self.rs_frames.get_color_frame()
            if not self.depth_image or not self.color_image:
                return
            self.work_depth_image = np.asanyarray(self.depth_image.get_data())
            self.work_image = np.asanyarray(self.color_image.get_data())

    def release_camera(self):
        if self.enable_realsense is not True:
            self.camera.release()
        else:
            self.rs_pipeline.stop()

    def display_frame(self):
        cv2.imshow("Ben Identifier", self.work_image)

    def predictBen(self):

        if not self.work_image:
            self.work_image = cv2.resize(self.work_image, (64, 64));
            image = cv2.cvtColor(self.work_image, cv2.COLOR_BGR2RGB)
            predict_image = scipy.misc.imresize(image, size=(self.num_px, self.num_px)).reshape((1, self.num_px*self.num_px*3)).T
            predict_image_result = BenIdentifier.helper.predict(predict_image, self.my_label_y, self.parameters)
            if self.liveTest is not True:
                return self.classes[int(np.squeeze(predict_image_result)), ].decode("utf-8")
            else:
                print(self.classes[int(np.squeeze(predict_image_result)), ].decode("utf-8"))

            return "notben"


def main():
    ben_ident = ben_identifier(camera=0, liveTest=True, enable_realsense=False)

    ben_ident.init_camera()

    while True:
        ben_ident.predictBen()
        ben_ident.display_frame()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()


#
#
#
# for file in os.listdir("./dataBen/TestImageRes"):
#     print(file)
#     if(count < 10):
#         my_label_y = [0]
#     else:
#         my_label_y = [1]
#     fname = "./dataBen/TestImageRes/" + file
#
#     image = np.array(ndimage.imread(fname, flatten=False))
#     my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
#
#     #my_predicted_image = predict(parameters["W2"], parameters["b2"], my_image)
#     my_predicted_image = predict(my_image, my_label_y, parameters)
#
#     plt.imshow(image)
#     print("y = " + str(np.squeeze(my_predicted_image)) + ", your algorithm predicts a \"" + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8") +  "\" picture.")
#
#     count += 1
#     print(count)
