import cv2
import numpy as np
import time
import skvideo.io
#suiii
videodata = skvideo.io.vread(r"C:\Users\alhar\OneDrive\Desktop\Typical junior tennis hook (forgot camera was up) ITA Summer Circuit UTR.mp4")
print(videodata.shape)

# Open the default camera (usually the webcam)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Initialize variables for storing the previous frame
previous_frame = None

# Capture video until the user presses 'q'
while True:
    time.sleep(0.250)  # Add a delay to reduce the frame rate

    # Capture frame-by-frame
    frame = videodata

    # If the frame was not captured properly, break the loop
    #if not ret:
    #    print("Error: Failed to capture the frame.")
    #    break

    # Apply GaussianBlur to reduce noise (optional)
    #blurred_frame = cv2.GaussianBlur(frame, (21, 21), 0)

    # If this is the first frame, initialize the previous_frame
    if previous_frame is None:
        previous_frame = frame
        continue

    # Compute the absolute difference between the current frame and the previous frame
    frame_diff = cv2.absdiff(previous_frame, frame)

    # Threshold the difference to get regions of interest
    _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill in holes and find contours
    thresh = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(thresh[:, :, 0], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a copy of the frame to draw the bounding boxes on it
    output_frame = frame.copy()

    # Draw bounding boxes around the contours where motion is detected
    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Ignore small contours (adjust as needed)
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

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
