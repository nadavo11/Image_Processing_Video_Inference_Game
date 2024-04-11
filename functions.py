
from webcam_stream import WebcamStream
import cv2
import numpy as np
import time
from scipy import ndimage
from pynput.keyboard import Key, Controller, Listener

# initializing and starting multi - thread webcam input stream
webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()

frame = webcam_stream.read()
H, W = frame.shape[:2]

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
        accepted = int(input("Enter 1 for OK, or 0 to retry: "))
        if accepted == 1:
            print(exp)
            break

    return background

def grid_output(frame, background):
    mask = filter_player(frame, background)
    #clean_mask, edges = create_clean_mask(mask)
    center_of_mass, width, height, percentage = get_player_position(mask)
    frame_with_rectangle = frame.copy()  # Copy the frame
    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):
        center_of_mass = (round(center_of_mass[0]), round(center_of_mass[1]))
        # Draw a green rectangle around the player's center of mass
        pt1 = (center_of_mass[0] - width//2, center_of_mass[1] - height//2)
        pt2 = (center_of_mass[0] + width//2, center_of_mass[1] + height//2)
        cv2.rectangle(frame_with_rectangle, pt1, pt2, (0, 255, 0), 2)  # Green color, thickness 2


    # Draw a red X at the player's center of mass
        frame_with_rectangle = cv2.drawMarker(frame_with_rectangle, center_of_mass, (0, 0, 255),
                                                  markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
        region =((center_of_mass[0] - width // 2,
                 center_of_mass[1] - height // 2),
                 (center_of_mass[0] + width // 2,
                 center_of_mass[1] ))
        cv2.rectangle(frame_with_rectangle,
                      region[0], region[1], (0, 150, 150), 2)  # Green color, thickness 2

        msk_region = mask[:center_of_mass[0], :]
        region_h = region[1][0] - region[0][0]

        uppermass_h, uppermass_w = np.where(msk_region == 255)

        # x,y are the center of x indices and y indices of mass pixels
        center_of_upper_mass = (np.average(uppermass_w), np.average(uppermass_h))
        # round the center of mass
        if not np.isnan(center_of_upper_mass[0]) and not np.isnan(center_of_upper_mass[1]):
            center_of_upper_mass = (round(center_of_upper_mass[0]), round(center_of_upper_mass[1]))

            # draw a red X at the player's center of upper mass
            frame_with_rectangle = cv2.drawMarker(frame_with_rectangle, center_of_upper_mass, (0, 0, 255),2)
    # Convert masks to BGR for display purposes
    binary_image1 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    binary_image2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Prepare frames for display
    frames = [background, frame, frame_with_rectangle, binary_image2]
    resized_frames = [cv2.resize(frame, (320, 240)) for frame in frames]

    # Combine frames into a grid
    top_row = np.hstack(resized_frames[:2])
    bottom_row = np.hstack(resized_frames[2:])
    grid = np.vstack((top_row, bottom_row))

    return grid, mask


######################

def get_player_position(mask,outlier_std_threshold=5):
    """
    :param mask: binary mask
    :return: (center_x, center_y)
    """
    # Find indices where we have mass
    mass_h, mass_w = np.where(mask == 255)


    # x,y are the center of x indices and y indices of mass pixels
    center_of_mass = (np.average(mass_w), np.average(mass_h)) #ndimage.measurements.center_of_mass(mask)#(np.average(mass_x), np.average(mass_y))

    if len(mass_w) < 10 or len(mass_h) < 10:
        #center_of_mass = (mask.shape[0]//2,mask.shape[1]//2)
        return center_of_mass, 10, 10, 0

    # Calculate distances of each pixel from the center of mass
    distances = np.sqrt((mass_h - center_of_mass[1]) ** 2 + (mass_w - center_of_mass[0]) ** 2)

    # Filter out outliers based on the standard deviation threshold
    std_dev = np.std(distances)
    #print("std_dev=",std_dev)
    main_mass_indices = np.where(distances <= outlier_std_threshold * std_dev)

    #mass_x_for_std = mass_x - center_of_mass[0]
    #mass_y_for_std = mass_y - center_of_mass[1]
    #std_x = np.std(mass_x_for_std)
    #std_y = np.std(mass_y_for_std)
    # Filter out outliers based on the threshold
    #distances =

    # Use only main mass indices to calculate width and height
    main_mass_w = mass_w[main_mass_indices]
    main_mass_h = mass_h[main_mass_indices]



    # Calculate percentage of mask pixels being equal to 1
    total_pixels = mask.shape[0] * mask.shape[1]
    ones_count = np.count_nonzero(mask)
    percentage = (ones_count / total_pixels) * 100

    # Calculate width and height of the rectangle
    if len(main_mass_w) < 50 or len(main_mass_h) < 50:
        width = 50
        height = 50
        return center_of_mass, width, height, percentage
    width = np.max(main_mass_w) - np.min(main_mass_w)
    height = np.max(main_mass_h) - np.min(main_mass_h)

    return center_of_mass, width, height, percentage

def player_lean(player_position, w = W, th = 5,mask = None,region = (0,0,H,W)):
    # calculate the threshold precentage
    th = w*th//100
    # height
    x = player_position[0]
    # width
    y = player_position[1]
    # operate in the region of the player's upper body
    # crop the image
    if not mask:
        return
    msk_region = mask[region[0][0]:region[1][0], region[1][0]:region[1][1]]
    region_h = region[1][0] - region[0][0]

    uppermass_h, uppermass_w = np.where(msk_region == 255)

    # x,y are the center of x indices and y indices of mass pixels
    center_of_upper_mass = (np.average(uppermass_h), np.average(uppermass_w))
    return center_of_upper_mass
    if y > W//2 + th:
        return 'right'
    if y < W//2 - th:
        return 'left'

def player_control(mask,keyboard):
    W = mask.shape[1]
    center_of_mass, width, height, percentage = get_player_position(mask)
    lean = 'center'
    # lean right and left
    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):

        lean = player_lean(center_of_mass,mask, W,region =((center_of_mass[0] - width // 2,
                                                            center_of_mass[1] - height // 2),
                                                           (center_of_mass[0] + width // 2,
                                                            center_of_mass[1] )))
    return lean
    if lean == 'left':
        print("left")
        keyboard.press_and_release(Key.left)
    if lean == 'right':
        print("right")
        keyboard.press_and_release(Key.right)
    '''
    if lean == 'left':
        print("left")
        keyboard.press_and_release(Key.left)
    # else:
    #     keyboard.on_release("l")
    if lean == 'right':
        print("right")
        keyboard.press_and_release(Key.right)
    # else:
    #     keyboard.on_release("r")
    '''
    # add controls here

