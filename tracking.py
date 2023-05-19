import cv2 as cv
import sys
import math
from timeit import default_timer as timer
(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
 
    if int(minor_ver) < 3:
        tracker = cv.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv.legacy.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv.TrackerCSRT_create()
 
    trackers={}
    # Read video
    video_path =  r"C:\Users\computer house\Downloads\vtest.avi"
    video = cv.VideoCapture(video_path)
 
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

   
bbox=cv.selectROI('Selecting ROIs',frame,False)
x1=bbox[0]+(bbox[2]//2)
y1=bbox[1]+(bbox[3]//2)
tracker.init(frame, tuple(bbox))
    

def speed(x1,y1,x2,y2,time):
    distance=math.sqrt((y2-y1)**2 +(x2-x1)**2)
    # time=1/fps
    speed=distance/time
    print("(x,y): (", round(x2,2),",",round(y2,2),")       Speed: ",round(speed,2))
    return round(speed,2)

while True:
    # Read a new frame
    ok, frame= video.read()
    if not ok:
        break

    # Create a copy of the frame to draw rectangles
    frame_copy = frame.copy()
    start=timer()

    
    ok, bbox = tracker.update(frame)
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        x2=bbox[0]+(bbox[2]//2)
        y2=bbox[1]+(bbox[3]//2)
        cv.rectangle(frame_copy, p1, p2, (255, 0, 0), 2, 1)
        check=True
    else:
        # Tracking failure
        cv.putText(frame_copy, "Tracking failure", (100, 80), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        check=False
    # Start timer
    timer1 = cv.getTickCount()

    # Update tracker
    # ok, bbox = tracker.update(frame)q

    # Calculate Frames per second (FPS)
    fps = cv.getTickFrequency() / (cv.getTickCount() - timer1)
    time=timer()-start
    # print("Time: ",time)
    # calculate speed
    if check:
        speed1=speed(x1,y1,x2,y2,time)
        x1=x2
        y1=y2

    # Display coordinates on frame
    cv.putText(frame_copy, "("+str(x1)+","+str(y1)+")", (100, 80), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Display speed on frame
    cv.putText(frame_copy, "Speed: "+str(speed1)+" pix/s", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    
    # Display tracker type on frame
    cv.putText(frame_copy, tracker_type + " Tracker", (100,20), cv.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
    
    # Display FPS on frame
    cv.putText(frame_copy, "FPS : " + str(int(fps)), (100,50), cv.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)

    # Display result
    cv.imshow("Tracking", frame_copy)

    # Exit if ESC pressed
    k = cv.waitKey(20) & 0xff
    if k ==  ord('q'): break

# Release the video capture
video.release()
cv.destroyAllWindows()