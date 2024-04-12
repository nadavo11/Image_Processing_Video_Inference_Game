from webcam_stream import WebcamStream
import cv2
import numpy as np
import time
from scipy import ndimage
from pynput.keyboard import Key, Controller, Listener
import Player_Position
from Player import Player


def filter_player(frame, background):
    # Compute the absolute difference of the current frame and background
    diff = cv2.absdiff(frame, background)
    # Convert the difference image to grayscale
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian filter to smooth the image
    diff_smoothed = cv2.GaussianBlur(diff_gray, (15, 15), 20)

    # Apply Median filter to further reduce noise
    diff_smoothed = cv2.medianBlur(diff_smoothed, 9)
    diff_smoothed = cv2.medianBlur(diff_smoothed, 9)
    diff_smoothed = cv2.medianBlur(diff_smoothed, 9)

    # Threshold the diff image so that we get the foreground
    _, thresh = cv2.threshold(diff_smoothed, 25, 255, cv2.THRESH_BINARY)

    return thresh


def scan_background(webcam_stream):
    # Capture the video frame

    frame = webcam_stream.read()
    background = frame.copy()
    # Get the dimensions of the frame
    height, width, _ = frame.shape
    # Calculate the position to center the text
    text_x = 0  # Adjust the multiplier as needed
    text_y = height // 2
    accepted = 0
    exp = webcam_stream.get_EXPOSURE()
    print(exp)
    webcam_stream.set_EXPOSURE(exp)
    while accepted != 1:
        for i in range(1000):
            frame = webcam_stream.read()
            background = frame.copy()
            # on the left side of the frame, write text
            # cv2.putText(frame, f'Do Not Stand In Frame {(500 - i)//50}', (410, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Do Not Stand In Frame {(1000 - i) // 100}', (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
            # Display the resulting frame
            cv2.imshow('output', frame)
            # quit the scan
            if cv2.waitKey(1) & 0xFF == ord('q'):
                webcam_stream.quit()
            if cv2.waitKey(1) & 0xFF == ord('1'):
                accepted = 1
                break

        frame = background.copy()
        # on the left side of the frame, write text
        cv2.putText(frame, f'This Is The Background : OK ? ', (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # Display the resulting frame
        cv2.imshow('output', frame)
        # quit the scan
        if cv2.waitKey(1) & 0xFF == ord('q'):
            webcam_stream.quit()
        exp = webcam_stream.get_EXPOSURE()
        # accepted = int(input("Enter 1 for OK, or 0 to retry: "))
        if cv2.waitKey(1) & 0xFF == ord('1'):
            accepted = 1
            print("accepted, and exp = ", exp)
            break

    return background


def draw_rectangle(frame, mask,center_of_mass,center_of_upper_mass, width, height):
    #center_of_mass, width, height, percentage = Player_Position.get_player_position(mask)
    frame_with_rectangle = frame.copy()  # Copy the frame
    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):
        center_of_mass = (round(center_of_mass[0]), round(center_of_mass[1]))
        # Draw a green rectangle around the player's center of mass
        pt1 = (center_of_mass[0] - width // 2, center_of_mass[1] - height // 2)
        pt2 = (center_of_mass[0] + width // 2, center_of_mass[1] + height // 2)
        cv2.rectangle(frame_with_rectangle, pt1, pt2, (0, 255, 0), 2)  # Green color, thickness 2

        # Draw a red X at the player's center of mass
        frame_with_rectangle = cv2.drawMarker(frame_with_rectangle, center_of_mass, (0, 0, 255),
                                              markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
        region = ((center_of_mass[0] - width // 2,
                   center_of_mass[1] - height // 2),
                  (center_of_mass[0] + width // 2,
                   center_of_mass[1]))
        cv2.rectangle(frame_with_rectangle,
                      region[0], region[1], (255, 0, 0), 2)  # Green color, thickness 2

        # Center of mass order (W,H)!!
        # Mask order (H,W) !!

        # round the center of mass
        if not np.isnan(center_of_upper_mass[0]) and not np.isnan(center_of_upper_mass[1]):
            center_of_upper_mass = (round(center_of_upper_mass[0]), round(center_of_upper_mass[1]))

            # draw a red X at the player's center of upper mass
            frame_with_rectangle = cv2.drawMarker(frame_with_rectangle, center_of_upper_mass, (0, 0, 255), 2)

    return frame_with_rectangle


def grid_output(frame, background, Mario):
    mask = filter_player(frame, background)
    Mario.mask = mask
    # clean_mask, edges = create_clean_mask(mask)


    # Convert masks to BGR for display purposes
    binary_image1 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    binary_image2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) ## It passes this one to display but calculate with Region mask
    frame_with_rectangle = frame.copy()
    center_of_mass, width, height, percentage = Player_Position.get_player_position(mask)
    mask = Player_Position.Region_mask(mask,center_of_mass,height,width)
    Mario.mask = mask
    Mario.center_of_mass = center_of_mass
    Mario.width = width
    Mario.height = height
    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):
        center_of_mass = (round(center_of_mass[0]), round(center_of_mass[1]))
        Mario.center_of_mass = center_of_mass
        lean, center_of_upper_mass = Player_Position.player_lean(center_of_mass,width, height,w=Mario.W, mask=mask)
        Mario.lean = lean
        Mario.center_of_upper_mass = center_of_upper_mass
        if lean == 'left':
            # paint binary image2 white pixels green
            binary_image2[mask == 255] = [0, 255, 0]
        if lean == 'right':
            # paint binary image2 white pixels red
            binary_image2[mask == 255] = [0,0,255]

        # edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        jumping = Player_Position.jumping(Mario)
        Mario.jump = jumping
        if not np.isnan(center_of_upper_mass[0]) and not np.isnan(center_of_upper_mass[1]):
            squat = Player_Position.player_squat(center_of_mass,center_of_upper_mass,th=1,H=Mario.H)
            Mario.squat = squat
            center_of_upper_mass = (round(center_of_upper_mass[0]), round(center_of_upper_mass[1]))
            Mario.center_of_upper_mass = center_of_upper_mass
            if squat == 'down':
                # draw arrow down
                binary_image2 = cv2.arrowedLine(binary_image2, center_of_upper_mass, center_of_mass, (0, 0, 255), 10,tipLength =0.5)

            if Mario.jump == 'up':
                binary_image2 = cv2.arrowedLine(binary_image2, center_of_mass, center_of_upper_mass, (0, 255, 0), 10,
                                                tipLength=0.5)
        frame_with_rectangle = draw_rectangle(frame, mask,center_of_mass,center_of_upper_mass, width, height)
    # Prepare frames for display
    frames = [background, frame, frame_with_rectangle, binary_image2]
    resized_frames = [cv2.resize(frame, (320, 240)) for frame in frames]

    # Combine frames into a grid
    top_row = np.hstack(resized_frames[:2])
    bottom_row = np.hstack(resized_frames[2:])
    grid = np.vstack((top_row, bottom_row))

    return grid, mask

######################
