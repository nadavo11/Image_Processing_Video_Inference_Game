import cv2
import numpy as np

def motion_detection(prev_frames, curr_frame, threshold=50):
    """
    Function to detect motion between consecutive frames.

    """

    # Convert frames to grayscale
    prev_gray_avg = np.mean(prev_frames, axis=0).astype(np.uint8)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference between current frame and average of previous frames
    diff = cv2.absdiff(prev_gray_avg, curr_gray)

    # Apply thresholding to create binary mask
    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Find contours of moving regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Analyze motion direction based on centroid movement
    motion_direction = None
    if contours:
        # Calculate centroid of the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0: # check if its a valid contour
            # Calculate centroid coordinates
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # Compare centroid position with frame width midpoint
            if cx < curr_frame.shape[1] // 2:
                motion_direction = 'Left'
            else:
                motion_direction = 'Right'

            # Draw contours on the current frame
            cv2.drawContours(curr_frame, [largest_contour], -1, (0, 255, 0), 2)

    return motion_direction, mask

# Example usage
cap = cv2.VideoCapture(0)
num_frames = 10  # Number of frames to compare
prev_frames = []

# Capture and preprocess initial frames
for _ in range(num_frames):
    _, frame = cap.read()
    prev_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

while True:
    _, curr_frame = cap.read()  # Capture current frame
    curr_frame = cv2.flip(curr_frame, 1)  # Flip horizontally

    motion_direction, mask = motion_detection(prev_frames, curr_frame)
    if motion_direction:
        print("Motion Direction:", motion_direction)

    # Display video feed
    cv2.imshow('Video Feed', curr_frame)

    # Display binary mask
    cv2.imshow('Binary Mask', mask)

    prev_frames.pop(0)  # Remove oldest frame from list
    prev_frames.append(cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY))  # Add current frame to list

    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
