import cv2
import os
count = 77
for f in os.listdir("./dataBen/BackTrain"):

    print(f)
    img = cv2.imread("./dataBen/BackTrain/" + f)
    img = cv2.resize(img, (64, 64));
    filename = ("./dataBen/BackTrainRes/" + str(count) + ".png")
    cv2.imwrite(filename, img)
    count = count + 1
    # cv2.imshow("test", img)
    # cv2.waitKey(1000);
    #img = cv2.imread(f)

##################################

#resize ben
#
# import cv2
# import os
# count = 10
# for f in os.listdir("./images"):
#
#     print(f)
#     img = cv2.imread("./images/" + f)
#     img = cv2.resize(img, (64, 64))
#
#     filename = ("./imagesRes/" + str(count) + ".png")
#     cv2.imwrite(filename, img)
#     count = count + 1
#     # cv2.imshow("test", img)
#     # cv2.waitKey(1000);
#     #img = cv2.imread(f)
