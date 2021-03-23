#!/usr/bin/python

import numpy as np
import cv2 as cv
from sys import argv
import time

# Reads /dev/video device index from first command line argument
dev_index = int(argv[1])
# Framerate is second command line argument
framerate = int(argv[2])
# Width from 3rd argument
width = int(argv[3])
# Height for 4th argument
height = int(argv[4])

# First try to open video capture from camera device /dev/video{device}
print("Creating video capture...")
video = cv.VideoCapture(dev_index)
print("Created video capture:", video)

while not video.isOpened():  # While camera is device is not opened
    print("Opening capture...")
    video.open(dev_index)  # Tries again to get video capture from device

print("Opened.")

while True:
    received, frame = video.read()  # Reads and waits for next captured frame
    if not received:  # No longer signal received from device, stops
        print("No signal from video stream.")
        break
    frame_recized = cv.resize(frame, (width, height))
    if height > 1: # we make sure that we can find left and right pixels
        array_top_pixels = frame_recized[0] # top pixels are the first row of the frame
        array_left_pixels = np.zeros((height-2, 3), dtype=np.uint8) # initialization of left pixels array with zeros and the right shape
        array_right_pixels = np.zeros((height-2, 3), dtype=np.uint8) # same for right pixels array
        for i in range(1, height-1, 1):
            array_left_pixels[i-1] = frame_recized[i][0] # left pixels are the first pixels of each row in the frame (except the first and last row)
            array_right_pixels[i-1] = frame_recized[i][width-1] # same but they are the last
        array_bottom_pixels = frame_recized[height-1] # bottom pixels are the last row of the frame
    else: #otherwise  everything in the same as the top pixels (the first row in the frame)
        array_top_pixels = frame_recized[0]
        array_left_pixels, array_right_pixels, array_bottom_pixels =  array_top_pixels, array_top_pixels, array_top_pixels
    # printing some info in the console
    print("pixels du haut :" , array_top_pixels)
    print("pixels de gauche :" , array_left_pixels)
    print("pixels de droite :" , array_right_pixels)
    print("pixels du bas :" , array_bottom_pixels)
    time.sleep(1/framerate)
