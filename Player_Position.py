
from webcam_stream import WebcamStream
import cv2
import numpy as np
import time
from scipy import ndimage
from pynput.keyboard import Key, Controller, Listener
import Frames_Process

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

    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):
        center_of_mass = (round(center_of_mass[0]), round(center_of_mass[1])) ## cancel if you want the accuracy
    return center_of_mass, width, height, percentage

def player_squat(center_of_mass,center_of_upper_mass,th=2,H=480):
    th = H * th // 50
    y = center_of_mass[1]
    if center_of_upper_mass[0] > y - th:
        print("center_of_upper_mass[0]=",center_of_upper_mass[0],"y=",y, "y-th=",y + th,"th=",th)
        return 'down'
    return 0
def player_lean(center_of_mass,width, height, w = 640 , th = 2,mask = None):
    # calculate the threshold precentage
    #print("W=",w)
    th = w*th//100
    # height
    x = center_of_mass[0]
    # width
    y = center_of_mass[1]
    # operate in the region of the player's upper body
    if mask is None:
        return
    # TODO: make this work:

    mask_region = Region_mask(mask,center_of_mass,height,width)

    uppermass_h, uppermass_w = np.where(mask_region == 255)

    # x,y are the center of x indices and y indices of mass pixels
    center_of_upper_mass = (np.average(uppermass_w), np.average(uppermass_h))
    if center_of_upper_mass[0] > x + th:
        return 'right',center_of_upper_mass
    if center_of_upper_mass[0] < x - th:
        return 'left',center_of_upper_mass
    return 'center', center_of_upper_mass

def player_control(mask,keyboard):
    W = mask.shape[1]
    H = mask.shape[0]
    #print("H=",H)
    center_of_mass, width, height, percentage = get_player_position(mask)
    lean = 'center'
    squat = 0
    # lean right and left
    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):

        lean,center_of_upper_mass = player_lean(center_of_mass,width, height, w=W,th=2,mask=mask)
        if not np.isnan(center_of_upper_mass[0]) and not np.isnan(center_of_upper_mass[1]):
            squat = player_squat(center_of_mass,center_of_upper_mass,th=2,H=H)

    #print(lean)
    if squat == 'down':
        print("down")
        keyboard.press_and_release(Key.down)
    if lean == 'left':
        print("left")
        keyboard.press_and_release(Key.left)
    if lean == 'right':
        print("right")
        keyboard.press_and_release(Key.right)

    # add controls here


def Region_mask(mask,center_of_mass,height,width):
    mask_region = np.zeros_like(mask)
    if not np.isnan(center_of_mass[0]) and not np.isnan(center_of_mass[1]):
        center_of_mass = (round(center_of_mass[0]), round(center_of_mass[1]))
        # Calculate the rectangle boundaries
        top = max(center_of_mass[1] - height // 2, 0)  # Ensure top is not less than 0
        bottom = min(center_of_mass[1], mask.shape[0])  # Ensure bottom does not exceed mask height
        left = max(center_of_mass[0] - width // 2, 0)  # Ensure left is not less than 0
        right = min(center_of_mass[0] + width // 2, mask.shape[1])  # Ensure right does not exceed mask width

        # Replace the region within the bounds with the corresponding values from the original mask
        mask_region[top:bottom, left:right] = mask[top:bottom, left:right]
    # iris
    return mask_region

