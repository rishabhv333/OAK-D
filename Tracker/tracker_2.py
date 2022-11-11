from collections import deque
import numpy as np
import argparse
import imutils
import cv2

try:
    import dhaiconswrap
    from dhaiconswrap import DeviceManager, docalibration, get_available_devices, domulticalibration

    assert (dhaiconswrap.__version__ == '0.2.2 '), " Update the dhaiconswrap package to version 0.2.2"
except:
    print("dhaiconswrap is not Installed...install using 'pip install dhaiconswrap'")

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default=None, help="ballTracker/video.mp4")
ap.add_argument("--size", default=(640, 400), help="OAK-D Frame Size")
ap.add_argument("--fps", default=30, help="OAK-D Frame FPS")
ap.add_argument("--calibration_mode", action='store_true', help="Execute OAK-D in calibration Mode")
ap.add_argument("--chessboard_params", default=[5, 8, 27], help="Chessboard parameters list(col,row,square[mm])")
ap.add_argument("--nn_mode", action='store_true', help="Run Neural Network inside the OAK-D")
ap.add_argument("--blob_path", default=None, help="Path to blob model to run edge neural networks on OAK-D")
ap.add_argument("--verbose", action='store_true', help="show device class info while creating instance")
args = ap.parse_args()

# pinkLower = (70, 88, 226)
# pinkUpper = (179, 255, 255)
pinkLower = (143, 18, 72)
pinkUpper = (179, 255, 255)
# pinkLower = (151, 83, 159)
# pinkUpper = (179, 255, 255)

if args.calibration_mode:
    args.size = (1920, 1080)

if args.nn_mode:
    if args.blob_path is None:
        raise 'A blob path is needed for internal inference! Insert the path to .blob file'
video = False
if args.video is not None:
    camera = cv2.VideoCapture(args["video"])
    video = True
else:
    cameras = {}
    available_devices = get_available_devices()
    if len(available_devices) > 1:
        for deviceid in available_devices:
            camera = DeviceManager(args.size, args.fps, deviceid, args.nn_mode, args.calibration_mode, args.blob_path,
                                   args.verbose)
            camera.enable_device()
            cameras[deviceid] = camera
    else:
        cameras = DeviceManager(args.size, args.fps, None, args.nn_mode, args.calibration_mode, args.blob_path,
                                args.verbose)
        cameras.enable_device()

if __name__ == '__main__':

    while True:

        if video:
            break
        if args.calibration_mode:
            if type(cameras) is dict:
                _ = domulticalibration(cameras, args.chessboard_params, [0, 0, 1080, 1920], [0, 0, 0], verbose=True)
                break
            else:
                _ = docalibration(cameras, args.chessboard_params, [0, 0, 1080, 1920], [0, 0, 0], verbose=True)
                break
        try:
            if type(cameras) is dict:
                break
            state, frames, results = cameras.pull_for_frames()
        except Exception as e:
            print(e)
        if state:
            font = cv2.FONT_HERSHEY_COMPLEX
            frame = imutils.resize(frames['color_image'], width=600)
            # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, pinkLower, pinkUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)

                if radius > 20:
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            detections = []
            for c in cnts:
                if cv2.contourArea(c) <= 80:
                    continue
                x, y, w, h = cv2.boundingRect(c)
                detections.append([0, 0.99, [x, y, x + w, y + h]])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # center = (x, y)
                # print(center)
            if results['points_cloud_data'] is not None:
                cameras.determinate_object_location(frame, results['points_cloud_data'], detections)

            # Showing the final image.

            cv2.imshow("Frame", frame)
            cv2.imshow("Object spatial position", frame)
            cv2.imshow("Mask", mask)
            cv2.imshow("Disparity", frames['disparity_image'])


            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                cameras.disable_device()
                break
    cv2.destroyAllWindows()
