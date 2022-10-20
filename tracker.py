from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import depthai as dai

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="ballTracker/video.mp4")
args = vars(ap.parse_args())

pinkLower = (70, 88, 226)
pinkUpper = (179, 255, 255)


def getFrame(queue):
    # Get frame from queue
    frame = queue.get()
    # Convert frame to OpenCV format and return
    return frame.getCvFrame()


def getMonoCamera(pipeline, isLeft):
    # Configure mono camera
    mono = pipeline.createMonoCamera()

    # Set Camera Resolution
    mono.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    if isLeft:
        # Get left camera
        mono.setBoardSocket(dai.CameraBoardSocket.LEFT)
    else:
        # Get right camera
        mono.setBoardSocket(dai.CameraBoardSocket.RIGHT)
    return mono


if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

if __name__ == '__main__':

    # Start defining a pipeline
    pipeline = dai.Pipeline()

    # Set up left and right cameras
    monoLeft = getMonoCamera(pipeline, isLeft=True)
    monoRight = getMonoCamera(pipeline, isLeft=False)

    with dai.Device(pipeline) as device:

        while True:
            grabbed, frame = camera.read()

            if args.get("video") and not grabbed:
                break
            font = cv2.FONT_HERSHEY_COMPLEX
            frame = imutils.resize(frame, width=600)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, pinkLower, pinkUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)

                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

            for c in cnts:
                if cv2.contourArea(c) <= 50:
                    continue
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center = (x, y)
                print(center)

            # Showing the final image.

            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()
