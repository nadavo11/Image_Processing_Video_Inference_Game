def filter_player(frame, background):
    # Convert RGB image to LAB color space
    frame_lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    background_lab = cv2.cvtColor(background, cv2.COLOR_BGR2LAB)
    # Compute the absolute difference of the current frame and background
    # diff = cv2.absdiff(frame, background)
    diff_A = np.abs(frame_lab[:, :, 1] - background_lab[:, :, 1])
    diff_B = np.abs(frame_lab[:, :, 2] - background_lab[:, :, 2])
    # Convert the difference image to grayscale
    # diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # diff_Agray = cv2.cvtColor(diff_A, cv2.COLOR_BGR2GRAY)
    # diff_Bgray = cv2.cvtColor(diff_B, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian filter to smooth the image
    diff_smoothed_A = cv2.GaussianBlur(diff_A, (15, 15), 20)
    diff_smoothed_B = cv2.GaussianBlur(diff_B, (15, 15), 20)

    # Apply Median filter to further reduce noise
    # diff_smoothed = cv2.medianBlur(diff_smoothed, 9)
    diff_smoothed_A = cv2.medianBlur(diff_smoothed_A, 9)
    diff_smoothed_B = cv2.medianBlur(diff_smoothed_B, 9)
    diff_smoothed = diff_smoothed_A + diff_smoothed_B
    # Threshold the diff image so that we get the foreground
    _, thresh = cv2.threshold(diff_smoothed, 40, 255, cv2.THRESH_BINARY)

    return thresh


def filter_player(frame, background):
    # Compute the absolute difference of the current frame and background
    diff = cv2.absdiff(frame, background)
    # Convert the difference image to grayscale
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian filter to smooth the image
    diff_smoothed = cv2.GaussianBlur(diff_gray, (15, 15), 20)

    # Apply Median filter to further reduce noise
    diff_smoothed = cv2.medianBlur(diff_smoothed, 9)

    # Threshold the diff image so that we get the foreground
    _, thresh = cv2.threshold(diff_smoothed, 25, 255, cv2.THRESH_BINARY)

    return thresh

def process_frame(frame, background):
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

'''    # Apply morphological operations
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)'''

def create_clean_mask(mask):
    # Apply edge detection
    edges = cv2.Canny(mask, 100, 200)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store the largest contour and its length
    max_length = 0
    max_contour = None

    # Iterate over the contours
    for contour in contours:
        # Calculate the length of the contour
        length = cv2.arcLength(contour, False)  # False indicates that the contour is not necessarily closed
        if length > max_length:
            # Update the maximum length and contour
            max_length = length
            max_contour = contour

    # Create an empty mask to draw the filled contour
    filled_mask = np.zeros_like(mask)

    # If a contour with non-zero length was found, draw it
    if max_contour is not None:
        cv2.drawContours(filled_mask, [max_contour], 0, (255), thickness=cv2.FILLED)

    return filled_mask, edges