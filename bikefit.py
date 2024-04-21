import cv2
import numpy as np
import math
import tkinter as tk#
from tkinter import filedialog


# Create a root Tk window and hide it
root = tk.Tk()
root.withdraw()

# Open file dialog to select the video file
video_file = filedialog.askopenfilename()

# Load the video
cap = cv2.VideoCapture(video_file)

# Create three trackers
tracker1 = cv2.TrackerMIL_create()
tracker2 = cv2.TrackerMIL_create()
tracker3 = cv2.TrackerMIL_create()

# Read the first frame
ret, frame = cap.read()

# Select three ROIs
bbox1 = cv2.selectROI("Tracking", frame, False)
bbox2 = cv2.selectROI("Tracking", frame, False)
bbox3 = cv2.selectROI("Tracking", frame, False)

# Initialize the trackers with the first frame and the bounding box
ok1 = tracker1.init(frame, bbox1)
ok2 = tracker2.init(frame, bbox2)
ok3 = tracker3.init(frame, bbox3)

# Initialize the list to store angles and the time counter
angles = []
time_counter = 0

while True:
    # Read a new frame
    ok, frame = cap.read()
    if not ok:
        break

    # Update trackers
    ok1, bbox1 = tracker1.update(frame)
    ok2, bbox2 = tracker2.update(frame)
    ok3, bbox3 = tracker3.update(frame)

    # Calculate the center of each bounding box
    center1 = (int(bbox1[0] + bbox1[2] / 2), int(bbox1[1] + bbox1[3] / 2))
    center2 = (int(bbox2[0] + bbox2[2] / 2), int(bbox2[1] + bbox2[3] / 2))
    center3 = (int(bbox3[0] + bbox3[2] / 2), int(bbox3[1] + bbox3[3] / 2))

    # Calculate vectors
    vector1 = np.array(center2) - np.array(center1)
    vector2 = np.array(center3) - np.array(center2)

    # Calculate angle
    angle = np.math.atan2(np.linalg.det([vector1,vector2]),np.dot(vector1,vector2))
    angle = np.degrees(angle)

    # Append the angle to the list and increment the time counter
    angles.append(angle)
    time_counter += 1

    # Draw bounding boxes and display the angle
    if ok1 and ok2 and ok3:
        cv2.rectangle(frame, (int(bbox1[0]), int(bbox1[1])), (int(bbox1[0] + bbox1[2]), int(bbox1[1] + bbox1[3])), (255,0,0), 2, 1)
        cv2.rectangle(frame, (int(bbox2[0]), int(bbox2[1])), (int(bbox2[0] + bbox2[2]), int(bbox2[1] + bbox2[3])), (255,0,0), 2, 1)
        cv2.rectangle(frame, (int(bbox3[0]), int(bbox3[1])), (int(bbox3[0] + bbox3[2]), int(bbox3[1] + bbox3[3])), (255,0,0), 2, 1)
        cv2.putText(frame, "Angle : " + str(angle), (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    else:
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display result
    cv2.imshow("Tracking", frame)

    # Exit if ESC key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the VideoCapture object
cap.release()

# Plot the angle over time
plt.plot(range(time_counter), angles)
plt.xlabel('Time')
plt.ylabel('Angle')
plt.title('Angle over Time')
plt.show()