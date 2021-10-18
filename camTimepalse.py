# Timelapse movie capture from WEBCAM.
# Working with WEBCAM connedted to Raspberry Pi machine.
# This code is working under Python 3 environment with OpenCV.
# The code will be invoked by cron everyday at AM6:00.
#
# Code history:
#   2020/Nov/?  S.Yamamoto  Original.
#   2021/Jan/1  S.Yamamoto  Using camera unit original resolution.

import cv2
import numpy as np
import sys
import datetime
import time

# Print header
print('Start timelapse at ', datetime.date.today())

# status number
args = sys.argv
if len(args) > 1:
    secondsPerFrame = float(args[1])
else:
    secondsPerFrame = 20
print( secondsPerFrame, ' seconds per frame.' )
nextFrameTime = time.time()

# Stop recording at 6:00PM
endHour = 18
print( 'Recording stop at ', endHour, ':00' )

# Stop recording after 12 hours.
dayEnd = time.time() + (12 * 60 * 60)
print( 'Recording stop at 12 hours later.' )

# Camera No.0
cap = cv2.VideoCapture(0)

# Get parameters
# fps = int(cap.get(cv2.CAP_PROP_FPS))
### 2021/1/1 Use default resolution
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1024)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
# cap.set(cv2.CAP_PROP_FPS, 30)

fps = 30.0
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('fps=', fps, '(w,h)=(', w, ',', h, ')' )

# Recording with MP4 format, but without H264 format.
# If used in HTML, the output movie must be converted to H264 format later.

fileName = '/home/pi/Project/python/' + str(datetime.date.today()) + '.mp4'
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

# fileName = '/home/pi/Project/python/' + str(datetime.date.today()) + '.avi'
# fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

out = cv2.VideoWriter(fileName, fourcc, fps, (w, h))

# font
font_scale = 0.5
color = (255, 255, 0)
thickness = 1

# Count loops
loop = 0
frameNumber = 0
while True:
    ret, frame = cap.read()
    superStr = str(datetime.datetime.now())[:16]
    cv2.putText( frame, superStr, (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)
    cv2.imshow('frame', frame)

    # Get frame and record if time reached to next frame time.
    if time.time() >= nextFrameTime:
        out.write(frame)
        nextFrameTime += secondsPerFrame
        # print( frameNumber )
        frameNumber += 1

    # Quit if 'q' key is typed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Quit if time reached to dayEnd time.
    dt_now = datetime.datetime.now()
    if dt_now.day == endHour:
        break

    if time.time() >= dayEnd:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
