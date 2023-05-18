import cv2 as cv
import sys

(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]
 
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
     
    bboxes = cv.selectROIs("Multi-Object Tracking", frame, False)
    for i, bbox in enumerate(bboxes):
        tracker = cv.TrackerKCF_create()
        trackers[i] = tracker
        trackers[i].init(frame, tuple(bbox))
    # # Define an initial bounding box
    # bbox = (287, 23, 86, 320)
 
    # # Uncomment the line below to select a different bounding box
    # bbox = cv.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Create a copy of the frame to draw rectangles
        frame_copy = frame.copy()

        for object_id, tracker in trackers.items():
            ok, bbox = tracker.update(frame)
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            else:
                # Tracking failure
                cv.putText(frame, "Object {} tracking failure".format(object_id), (100, 80),
                            cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
         
        # Start timer
        timer = cv.getTickCount()
 
        # Update tracker
        # ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv.getTickFrequency() / (cv.getTickCount() - timer)
 
        # # Draw bounding box
        # if ok:
        #     # Tracking success
        #     p1 = (int(bbox[0]), int(bbox[1]))
        #     p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        #     cv.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        # else :
        #     # Tracking failure
        #     cv.putText(frame, "Tracking failure detected", (100,80), cv.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv.putText(frame, tracker_type + " Tracker", (100,20), cv.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        # Display FPS on frame
        cv.putText(frame, "FPS : " + str(int(fps)), (100,50), cv.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
 
        # Display result
        cv.imshow("Tracking", frame_copy)
 
        # Exit if ESC pressed
        k = cv.waitKey(5) & 0xff
        if k ==  ord('q'): break

# Release the video capture
video.release()
cv.destroyAllWindows()