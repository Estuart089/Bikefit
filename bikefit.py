import cv2
import numpy as np

import tkinter as tk
from tkinter import filedialog

# Create a root Tk window and hide it
root = tk.Tk()
root.withdraw()

# Open file dialog to select the video file
video_file = filedialog.askopenfilename()


# Load the video
cap = cv2.VideoCapture(video_file)

# Create a tracker
tracker = cv2.TrackerMIL_create()

# Read the first frame
ret, frame = cap.read()

# Select ROI
bbox = cv2.selectROI("Tracking", frame, False)
ok = tracker.init(frame, bbox)


while True:
    # Read a new frame
    ok, frame = cap.read()
    if not ok:
        break

    # Update tracker
    ok, bbox = tracker.update(frame)

    # Draw bounding box
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    else:
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display result
    cv2.imshow("Tracking", frame)

    # Exit if ESC key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the VideoCapture object
cap.release()