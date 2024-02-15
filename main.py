from webcam_stream import WebcamStream
import cv2
import numpy as np

print("hello github")

# initializing and starting multi - thread webcam input stream
webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()

frame = webcam_stream.read()
H, W = frame.shape[:2]

def filter_player(frame, background):
    # Convert frame to grayscale for easier comparison
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert background to grayscale for easier comparison
    background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference of the current frame and background
    diff = cv2.absdiff(frame_gray, background_gray)

    # Threshold the diff image so that we get the foreground
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

    return thresh
def scan_background(webcam_stream):
    # Capture the video frame
    frame = webcam_stream.read()
    background = frame.copy()

    # scan the left side of the frame
    for i in range(500):
        frame = webcam_stream.read()

        # left side of the frame
        background[:, : W // 2] = frame[:, : W // 2]

        # on the left side of the frame, write text
        cv2.putText(frame, f'stand here {(500 - i)//50}', (410, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # draw a line in the middle of the frame
        cv2.line(frame, (W // 2, 0), (W // 2, H), (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('output', frame)

        # quit the scan
        if cv2.waitKey(1) & 0xFF == ord('q'):
            webcam_stream.quit()

    # scan the right side of the frame
    for i in range(500):
        frame = webcam_stream.read()
        # right side of the frame
        background[:, W // 2:] = frame[:, W // 2:]

        # on the left side of the frame, write text
        cv2.putText(frame, f'stand here {(500 - i)//50}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        # draw a line in the middle of the frame
        cv2.line(frame, (W // 2, 0), (W // 2, H), (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('output', frame)

        # quit the scan
        if cv2.waitKey(1) & 0xFF == ord('q'):
            webcam_stream.quit()

    # press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        webcam_stream.quit()

    return background


def play():
    # Convert background to grayscale for easier comparison
    background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    print("Press 'q' to quit")
    while (True):
        # Capture the video frame
        frame = webcam_stream.read()
        mask = filter_player(frame, background)
        cv2.imshow('output', mask)

        # press q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            webcam_stream.quit()


background = scan_background(webcam_stream)
play()
# After the loop release the cap object
webcam_stream.vcap.release()
# Destroy all the windows
cv2.destroyAllWindows()
