from BenIdentifier.helper import *
import os
import csv
import scipy
from scipy import ndimage
import pickle
import cv2
import sys
import rospy
num_px = 64;

parameters = pickle.load( open( "/home/turtlebot/catkin_ws/src/i2c_lcd/BenIdentifier/weights.p", "rb" ))
train_x_orig, train_y, test_x_orig, test_y, classes = load_data()

count = 0;

cam = cv2.VideoCapture(3)   # 0 -> index of camera

def predictBen():
    my_label_y = [1]
    s, img = cam.read()
    cv2.waitKey(10)

    k = cv2.waitKey(33)
    if (k==27):    # Esc key to stop
        cam.release()
        cv2.destroyAllWindows()
        rospy.signal_shutdown("exit cv2")
        sys.exit()

    if s:
        #cv2.imshow("test", img)
        cv2.waitKey(10)

    img = cv2.resize(img, (64, 64));
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
    my_predicted_image = predict(my_image, my_label_y, parameters)

    #print(classes[int(np.squeeze(my_predicted_image)),].decode("utf-8"))
    return classes[int(np.squeeze(my_predicted_image)),].decode("utf-8")


liveTest = False
while(liveTest):

    my_label_y = [1]
    s, img = cam.read()
    cv2.waitKey(10)
    if s:    # frame captured without any errors
        cv2.imshow("BEN?", img)
        cv2.waitKey(10)

    img = cv2.resize(img, (64, 64));
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #fname = "./tempimg.png"

    #image = np.array(ndimage.imread(fname, flatten=False))
    #fname = "./tempimg.png"
    #image = np.array(ndimage.imread(fname, flatten=False))
    my_image = scipy.misc.imresize(image, size=(num_px,num_px)).reshape((1, num_px*num_px*3)).T
    my_predicted_image = predict(my_image, my_label_y, parameters)

    #print("y = " + str(np.squeeze(my_predicted_image)) + ", your algorithm predicts a \"" + classes[int(np.squeeze(my_predicted_image)),].decode("utf-8") +  "\" picture.")
    print(classes[int(np.squeeze(my_predicted_image)),].decode("utf-8"))
    count += 1
    #print(count)


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
