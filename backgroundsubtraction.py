# This program illustrates how to capture frames in a video stream and how to do further processing on them
# It uses numpy to do the calculations and OpenCV to display the frames

import picamera
import picamera.array                           # This needs to be imported explicitly
import time
import cv2
import numpy as np
from headMovement import *




# Initialize the camera
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
camera.vflip = False                            # Flip upside down or not
camera.hflip = True                             # Flip left-right or not


# Create a data structure to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(320, 240))
width = 320
height = 240


# Allow the camera to warm up
time.sleep(0.1)

lowerColorThreshold = np.array([100, 100, 100])
upperColorThreshold = np.array([255, 255, 255])


if __name__ == '__main__':
    try:
        
        # Continuously capture frames from the camera
        # Note that we chose the RGB format
        initbackground = 1
        for frame in camera.capture_continuous(rawframe, format = 'rgb', use_video_port = True):

            # Clear the rawframe in preparation for the next frame
            rawframe.truncate(0)

            # Create a numpy array representing the image
            np = frame.array
            np.setflags(write=1)
            
            np[:,:,0] = np[:,:,0] * 0.21 + np[:,:,1] * 0.71 + + np[:,:,2] * 0.08
            np[:,:,1] = np[:,:,0]
            np[:,:,2] = np[:,:,0]
            #np_sub = np
            #newnp_sub = np_sub
            if initbackground == 1:
                np_background = np
                initbackground = 0
            else:
                np = np - np_background
                mask = cv2.inRange(np, lowerColorThreshold, upperColorThreshold)
                
                leftPixels = cv2.countNonZero(mask[:, 0:width//3])
                print("leftPixels =", leftPixels)

                rightPixels = cv2.countNonZero(mask[:,(width//3*2):width])
                print("rightPixels =", rightPixels)

                if (leftPixels > rightPixels):
                    left()
                    #time.sleep()
                elif (rightPixels > leftPixels):
                    #time.sleep(1)
                    if (rightPixels == 25920) and (leftPixels == 25440):
                        middle()
                    else:
                        right()
                else:
                    middle()
                    #time.sleep(1)
                
                
                #np = (np > np_background)
                """for x in range(0, len(np_sub[0]), 5000):
                    for y in range(0, len(np_sub[1]), 5000):
                        for a in range(35):
                            for b in range(6):
                                [R,G,B] = np_sub[a][b]
                                if [R,G,B] < [10,10,10]:
                                    newnp_sub[a][b] = [0,0,0]
                                else:
                                    newnp_sub[a][b] = [255,255,255]
"""
               # cv2.imshow("current frame", np[:,:,::-1])
                cv2.imshow("current frame", mask[:,:])

                    


                cv2.waitKey(1)




    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        camera.close()
        print("Program stopped by User")
        cv2.destroyAllWindows()
        # Clean up the camera resources
