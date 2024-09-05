import cv2
import numpy as np
import time
import skvideo.io
#sd
# Load the video file
videodata = skvideo.io.vread(r"C:\Users\alhar\OneDrive\Desktop\Typical junior tennis hook (forgot camera was up) ITA Summer Circuit UTR.mp4")
print(videodata.shape)
 
# Initialize variables for storing the previous frame
previous_frame = None

# Iterate through each frame in the video
for i, frame in enumerate(videodata):  # Add a delay to reduce the frame rate
    time.sleep(0.030)
    # If this is the first frame, initialize the previous_frame
    if previous_frame is None:
        previous_frame = frame
        continue

    # Compute the absolute difference between the current frame and the previous frame
    frame_diff = cv2.absdiff(previous_frame, frame)

    # Threshold the difference to get regions of interest
    _, thresh = cv2.threshold(frame_diff, 20, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill in holes and find contours
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh[:, :, 0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a copy of the frame to draw the bounding boxes on it
    output_frame = frame.copy()

    # Draw bounding boxes around the contours where motion is detected
    for contour in contours:
        if cv2.contourArea(contour) < 120:  # Ignore small contours (adjust as needed)
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame with bounding boxes
    cv2.imshow('Motion Detection', output_frame)
    cv2.imshow("White and Black Pixels", thresh)

    # Update the previous frame to the current frame
    previous_frame = frame

    # Exit the loop when the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
