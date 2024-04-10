
from webcam_stream import WebcamStream
import cv2
import numpy as np
import time

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
    # Convert masks to BGR for display purposes
    binary_image1 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    binary_image2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Prepare frames for display
    frames = [background, frame, binary_image1, binary_image2]
    resized_frames = [cv2.resize(frame, (320, 240)) for frame in frames]

    # Combine frames into a grid
    top_row = np.hstack(resized_frames[:2])
    bottom_row = np.hstack(resized_frames[2:])
    grid = np.vstack((top_row, bottom_row))

    return grid, mask


######################
def get_player_position(mask):
    """
    :param mask: binary mask
    :return: (center_x, center_y)
    """
    # Find indices where we have mass
    mass_x, mass_y = np.where(mask == 255)

    # x,y are the center of x indices and y indices of mass pixels
    center_of_mass = (np.average(mass_x), np.average(mass_y))
    return center_of_mass

def player_lean(player_position, w = W, th = 5):
    # calculate the threshold precentage
    th = w*th//100
    # height
    x = player_position[0]
    # width
    y = player_position[1]

    if y > W//2 + th:
        return 'right'
    if y < W//2 - th:
        return 'left'

def player_control(mask,keyboard):
    W = mask.shape[1]
    position = get_player_position(mask)

    # lean right and left
    lean = player_lean(position, W)

    if lean == 'left':
        print("left")
        keyboard.set_hexKeyCode("left")
        keyboard.pressNrelease()
    if lean == 'right':
        keyboard.set_hexKeyCode("right")
        keyboard.pressNrelease()


    # add controls here
