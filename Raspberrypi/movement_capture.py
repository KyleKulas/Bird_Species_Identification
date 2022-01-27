# Description: This algorithm detects moving object from the raspberry Pi camera
# using the Gaussian Mixture Model background subtraction method. 

from picamera.array import PiRGBArray 
from picamera import PiCamera 
import time 
import cv2 
import numpy as np 
from os import listdir, path

# parameters
min_detection_area_threshold = 20000 # minimum contour area that will trigger image saving
resolution = (512, 512)             # max 2592 × 1944 pixels
frame_rate = 15
subtractor_history = 50
save_path = 'frames_with_movement/'


#check files in save directory to get next file number
files = listdir(save_path)
jpg_files = [file.split('.')[0] for file in files if file.split('.')[1] == 'jpg']
jpg_files.sort()
try:
    last_count = int(jpg_files[-1])
except IndexError:
    count = 0
else:
    count = last_count + 1


# Initialize the camera
camera = PiCamera()
camera.resolution = resolution
camera.framerate = frame_rate
raw_capture = PiRGBArray(camera, size=resolution)
 
# Create the background subtractor object
back_sub = cv2.createBackgroundSubtractorMOG2(history=subtractor_history,
  varThreshold=15, detectShadows=False)
 
kernel = np.ones((20,20),np.uint8)

time.sleep(1)

# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
     
    # Grab the raw NumPy array representing the image
    image = frame.array
 
    # Convert to foreground mask. black white image. white is different from background, ie movement
    fg_mask = back_sub.apply(image)
     
    # Close gaps using closing
    fg_mask = cv2.morphologyEx(fg_mask,cv2.MORPH_CLOSE,kernel)
       
    # Remove salt and pepper noise with a median filter
    fg_mask = cv2.medianBlur(fg_mask,5)
       
    # If a pixel is less than ##, it is considered black (background). 
    # Otherwise, it is white (foreground). 255 is upper limit.
    _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)
 
    # Find the contours of the object inside the binary image
    contours, hierarchy = cv2.findContours(fg_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    areas = [cv2.contourArea(c) for c in contours]
    
    
    # If there are no countours
    if len(areas) < 1:
        
        cv2.imshow('Frame',image)
        key = cv2.waitKey(1) & 0xFF

        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

        if key == ord("q"):
            break       

        continue
  
    # if the are contours 
    else:
         
        max_index = np.argmax(areas)
        cnt = contours[max_index]

        # Get bounding circle of moving object
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        x, y  = center[0] - radius, center[1]-radius
        height, width = radius * 2, radius * 2
        
        # Crop image using bounding circle coordinates
        if width * height > min_detection_area_threshold:

            if center[0] - radius < 0 or center[0] + radius > resolution[0] or center[1] - radius < 0 or center[1] + radius > resolution[1]:
                # bounding cirlce outside frame
                pass
            else:
                roi = image[y:y + height, x:x + width]   
                cropped = cv2.resize(roi, (256,256))
                cv2.imshow("Frame",cropped)
                cv2.imwrite(f'{save_path}{count}.jpg', cropped)
                count += 1
                frames_since_last_capture = 0
        
        # Wait for keyPress for 1 millisecond
        key = cv2.waitKey(1) & 0xFF
    
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

        if key == ord("q"):
            break

        
# Close down windows
cv2.destroyAllWindows()