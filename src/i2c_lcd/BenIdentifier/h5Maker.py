
import h5py
import cv2
import numpy as np
import os
f = h5py.File("benTrainSet.h5", "w")
length = 100
################################################################################
print("--------------------------")
print("Yset Print")

yset = f.create_dataset("train_set_y", (length,), dtype='int64')
for i in range (length):
    if(i > 76):
        yset[i] = 1 #not ben
    else:
        yset[i] = 0 #ben

print("Name: " + yset.name)
print("Shape: " + str(yset.shape))
print("Type: " + str(yset.dtype))
print("0th Shape: " + str(yset[0].shape))

################################################################################
print("--------------------------")
print("Xset Print")
xset = f.create_dataset("train_set_x", (length, 64, 64, 3), dtype='uint8')
print("Name: " + xset.name)
print("Shape: " + str(xset.shape))
print("Type: " + str(xset.dtype))
print("0th Shape: " + str(xset[0].shape))
count = 0;
for file in os.listdir("./dataBen/AllTrainRes"):
    print(file)
    img = cv2.imread("./dataBen/AllTrainRes/" + file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    xset[count] = img
    count += 1

################################################################################
# print("--------------------------")
# print("Classes Print") # for test set
# cset = f.create_dataset("list_classes", (2,), dtype='|S7')
# print("Name: " + cset.name)
# print("Shape: " + str(cset.shape))
# print("Type: " + str(cset.dtype))
# print("0th Shape: " + str(cset[0].shape))
# cset[0] = b'ben'
# cset[1] = b'notben'




################################################################################
print("--------------------------")
print(f.keys())
