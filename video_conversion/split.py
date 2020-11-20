import cv2
import numpy as np
import os

def get_frames(film_file):
    # Playing video from file:
    cap = cv2.VideoCapture(film_file)

    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')

    currentFrame = 0
    while(True):
        try:

        # Capture frame-by-frame
            ret, frame = cap.read()

        # Saves image of the current frame in jpg file
            name = './data/frame' + str(currentFrame) + '.jpg'
            cv2.imwrite(name, frame)

        # To stop duplicate images
            currentFrame += 1
        except:
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()