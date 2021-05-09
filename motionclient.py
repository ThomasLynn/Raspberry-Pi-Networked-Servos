# Python program to implement 
# Webcam Motion Detector
# Taken from https://www.geeksforgeeks.org/webcam-motion-detector-python/
# This code has been modified to detect changes in the image
# from frame-to-frame instead of from the starting frame
# various enhancements have been made to make this more reliable
# (such as stacking the differences of multiple frames)
  
# importing OpenCV, time and Pandas library
import cv2, time, pandas
import numpy as np
import socket
# importing datetime class from datetime library
from datetime import datetime
import client

# Number of (old) diff_frames to use
# Set to 1 for no old diff_frames
num_diff_frames = 4

# Threshold for difference
# increase this if using more num_diff_frames
threshold_value = 20



# Assigning our static_back to None
static_back = None

# List of all the old diff_frames
diff_frames = []
  
# Time of movement
time = []
  
# Initializing DataFrame, one column is start 
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])
  
# Capturing video
video = cv2.VideoCapture(0)

# from https://stackoverflow.com/questions/44865023/how-can-i-create-a-circular-mask-for-a-numpy-array
def create_circular_mask(h, w, center=None, radius=None):

    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    mask = np.array(mask, dtype = np.uint8)
    return mask
    
#kernel = np.ones((45,45),np.uint8)
kernel = create_circular_mask(45,45)
kernel_laser = create_circular_mask(53,53)
 
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # Connect to server and send data
    sock.connect((client.HOST, client.PORT))
    client.set_socket(sock)
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
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)
      
        # In first iteration we assign the value 
        # of static_back to our first frame
        if static_back is None:
            static_back = blurred
            continue
      
        # Difference between static background 
        # and current frame(which is GaussianBlur)
        static_back_copy_non_red = static_back.copy()
        static_back_copy_non_red[:,:,2] = 0
        blurred_copy_non_red = blurred.copy()
        blurred_copy_non_red[:,:,2] = 0
        diff_frame_non_red = cv2.absdiff(static_back_copy_non_red, blurred_copy_non_red)
        
        blurred_copy_red = blurred.copy()
        blurred_copy_red[:,:,:2] = 0
        blurred_copy_red = cv2.threshold(blurred_copy_red, 200, 255, cv2.THRESH_BINARY)[1]
        blurred_copy_red = cv2.dilate(blurred_copy_red, kernel_laser, iterations = 1)
        blurred_copy_red[:,:,0] = blurred_copy_red[:,:,2]
        blurred_copy_red[:,:,1] = blurred_copy_red[:,:,2]
        
        diff_frame = (diff_frame_non_red.astype(np.int32) * (blurred_copy_red==0)).clip(0, 255).astype(np.uint8)
        
        diff_frame = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY) ###
        #diff_frame = cv2.GaussianBlur(diff_frame, (11, 11), 0)
        
        diff_frames.append(diff_frame)
        if len(diff_frames)>num_diff_frames:
            diff_frames.pop(0)
        
        diff_frame = np.zeros((480,640),dtype = np.uint8)
        
        for i in range(0,len(diff_frames)):
            diff_frame += diff_frames[i]
        
      
        # If change in between static background and
        # current frame is greater than 30 it will show white color(255)
        thresh_frame = cv2.threshold(diff_frame, threshold_value, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, kernel, iterations = 2)
      
        # Finding contour of moving object
        cnts,_ = cv2.findContours(thresh_frame.copy(), 
                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      
        frame_cnt = np.array(frame)
        
        biggest = None
        biggest_size = None
        for contour in cnts:
            #if cv2.contourArea(contour) < 10000:
            if cv2.contourArea(contour) < 1000:
                continue
            motion = 1
      
            (x, y, w, h) = cv2.boundingRect(contour)
            if biggest is None or w*h>biggest_size:
                biggest = contour
                biggest_size = w*h
            # making green rectangle arround the moving object
            cv2.rectangle(frame_cnt, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
         
        if biggest is not None:
            client.set_pos(x+w/2, y+h/2, frame.shape)
      
        # Displaying color frame with contour of motion of object
        cv2.imshow("Color Frame (1)", frame)
      
        # Displaying image in gray_scale
        cv2.imshow("Non Red Difference (2)", diff_frame_non_red)
      
        # Displaying image in gray_scale
        cv2.imshow("Red Laser Filter (3)", blurred_copy_red.astype(np.uint8))
      
        # Displaying the difference in currentframe to
        # the staticframe(very first_frame)
        cv2.imshow("Difference Frame (4)", diff_frame)
      
        # Displaying the black and white image in which if
        # intensity difference greater than 30 it will appear white
        cv2.imshow("Threshold Frame (5)", thresh_frame)
      
        # Displaying image in gray_scale
        cv2.imshow("Contour Frame (6)", frame_cnt)
      
        key = cv2.waitKey(1)
        # if q entered whole process will stop
        if key == ord('q'):
            # if something is movingthen it append the end time of movement
            if motion == 1:
                time.append(datetime.now())
            break
        if key == ord('w'):
            client.servo_zero_positions[1] -=1
            client.servo_distance[1] +=1
            print("xy",client.servo_zero_positions,client.servo_distance)
        if key == ord('s'):
            client.servo_zero_positions[1] +=1
            client.servo_distance[1] -=1
            print("xy",client.servo_zero_positions,client.servo_distance)
        if key == ord('d'):
            client.servo_zero_positions[0] -=1
            client.servo_distance[0] +=1
            print("xy",client.servo_zero_positions,client.servo_distance)
        if key == ord('a'):
            client.servo_zero_positions[0] +=1
            client.servo_distance[0] -=1
            print("xy",client.servo_zero_positions,client.servo_distance)
        if key == ord('g'):
            client.servo_distance[1] +=1
            print("xy",client.servo_zero_positions,client.servo_distance)
        if key == ord('t'):
            client.servo_distance[1] -=1
            print("xy",client.servo_zero_positions,client.servo_distance)
        if key == ord('f'):
            client.servo_distance[0] +=1
            print("xy",client.servo_zero_positions,client.servo_distance)
        if key == ord('h'):
            client.servo_distance[0] -=1
            print("xy",client.servo_zero_positions,client.servo_distance)
            
        static_back = blurred # now dects difference between this frame and last
 
  
video.release()
  
# Destroying all the windows
cv2.destroyAllWindows()
