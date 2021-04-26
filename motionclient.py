# Python program to implement 
# Webcam Motion Detector
# Taken from https://www.geeksforgeeks.org/webcam-motion-detector-python/
  
# importing OpenCV, time and Pandas library
import cv2, time, pandas
import numpy as np
# importing datetime class from datetime library
from datetime import datetime

# Number of (old) diff_frames to use
# Set to 1 for no old diff_frames
num_diff_frames = 4

# Threshold for difference
# increase this if using more num_diff_frames
threshold_value = 40



# Assigning our static_back to None
static_back = None

# List of all the old diff_frames
diff_frames = []
  
# List when any moving object appear
motion_list = [ None, None ]
  
# Time of movement
time = []
  
# Initializing DataFrame, one column is start 
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])
  
# Capturing video
video = cv2.VideoCapture(0)
  
# Infinite while loop to treat stack of image as video
while True:
    # Reading frame(image) from video
    check, frame = video.read()
  
    # Initializing motion = 0(no motion)
    motion = 0
  
    # Converting color image to gray_scale image
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
    # Converting gray scale image to GaussianBlur 
    # so that change can be find easily
    #gray = cv2.GaussianBlur(gray, (21, 21), 0)
    #gray = cv2.GaussianBlur(gray, (31, 31), 0)
    gray = cv2.GaussianBlur(frame, (21, 21), 0)
  
    # In first iteration we assign the value 
    # of static_back to our first frame
    if static_back is None:
        static_back = gray
        continue
  
    # Difference between static background 
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray)
    diff_frame = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY) ###
    
    diff_frames.append(diff_frame)
    if len(diff_frames)>num_diff_frames:
        diff_frames.pop(0)
    
    diff_frame = np.zeros((480,640),dtype = np.uint8)
    
    for i in range(0,len(diff_frames)):
        diff_frame += diff_frames[i]
    
  
    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
    #thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.threshold(diff_frame, threshold_value, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((45,45),np.uint8)
    #thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    thresh_frame = cv2.dilate(thresh_frame, kernel, iterations = 2)
  
    # Finding contour of moving object
    cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
    for contour in cnts:
        #if cv2.contourArea(contour) < 10000:
        if cv2.contourArea(contour) < 1000:
            continue
        motion = 1
  
        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
  
    # Appending status of motion
    motion_list.append(motion)
  
    motion_list = motion_list[-2:]
  
    # Appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        time.append(datetime.now())
  
    # Appending End time of motion
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        time.append(datetime.now())
  
    # Displaying image in gray_scale
    cv2.imshow("Gray Frame", gray)
  
    # Displaying the difference in currentframe to
    # the staticframe(very first_frame)
    cv2.imshow("Difference Frame", diff_frame)
  
    # Displaying the black and white image in which if
    # intensity difference greater than 30 it will appear white
    cv2.imshow("Threshold Frame", thresh_frame)
  
    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)
  
    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        # if something is movingthen it append the end time of movement
        if motion == 1:
            time.append(datetime.now())
        break
        
    static_back = gray # now dects difference between this frame and last
  
# Appending time of motion in DataFrame
for i in range(0, len(time), 2):
    df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True)
  
# Creating a CSV file in which time of movements will be saved
df.to_csv("Time_of_movements.csv")
  
video.release()
  
# Destroying all the windows
cv2.destroyAllWindows()