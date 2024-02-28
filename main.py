from webcam_stream import WebcamStream
from functions import filter_player, scan_background
import cv2
import numpy as np

print("hello github")
print("hello github2")

# initializing and starting multi - thread webcam input stream
webcam_stream = WebcamStream(stream_id=0)  # 0 id for main camera
webcam_stream.start()

frame = webcam_stream.read()
H, W = frame.shape[:2]

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
