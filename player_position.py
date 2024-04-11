from functions import H,W
from webcam_stream import WebcamStream
import cv2
import numpy as np
import time
from scipy import ndimage
from pynput.keyboard import Key, Controller, Listener

def get_player_position(mask,outlier_std_threshold=5):
    """
    :param mask: binary mask
    :return: (center_x, center_y)
    """
    # Find indices where we have mass
    mass_h, mass_w = np.where(mask == 255)

    # x,y are the center of x indices and y indices of mass pixels
    center_of_mass = (np.average(mass_w), np.average(mass_h))

    if len(mass_w) < 10 or len(mass_h) < 10:
        #center_of_mass = (mask.shape[0]//2,mask.shape[1]//2)
        return center_of_mass, 10, 10, 0

    # Calculate distances of each pixel from the center of mass
    distances = np.sqrt((mass_h - center_of_mass[1]) ** 2 + (mass_w - center_of_mass[0]) ** 2)

    # Filter out outliers based on the standard deviation threshold
    std_dev = np.std(distances)
    main_mass_indices = np.where(distances <= outlier_std_threshold * std_dev)

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

def player_lean(player_position, w = W, th = 2,mask = None,region = (0,0,H,W)):
    # calculate the threshold precentage
    th = w*th//100
    # height
    x = player_position[0]
    # width
    y = player_position[1]
    # operate in the region of the player's upper body
    # crop the image
    if mask is None:
        return
    # TODO: make this work:
    # round region
    # region = ((round(region[0][0]),round(region[0][1])),(round(region[1][0]),round(region[1][1])))
    # msk_region = mask[region[1][1]:region[1][1], region[0][0]:region[0][1]]
    region_h = region[1][0] - region[0][0]

    msk_region = mask[:round(x), :]
    region_h = region[1][0] - region[0][0]

    uppermass_h, uppermass_w = np.where(msk_region == 255)

    # x,y are the center of x indices and y indices of mass pixels
    center_of_upper_mass = (np.average(uppermass_h), np.average(uppermass_w))
    if center_of_upper_mass[1] > x + th:
        return 'right'
    if center_of_upper_mass[1] < x - th:
        return 'left'
    return 'center'

def player_control(mask,keyboard):
    W = mask.shape[1]
    center_of_mass, width, height, percentage = get_player_position(mask)
    lean = 'center'
    # lean right and left
    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):

        lean = player_lean(center_of_mass,mask=mask,th=2, w=W,region =((center_of_mass[0] - width // 2,
                                                            center_of_mass[1] - height // 2),
                                                           (center_of_mass[0] + width // 2,
                                                            center_of_mass[1] )))
    print(lean)
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

