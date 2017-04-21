import threading

import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import os
import cv2


class Camera:
    thread = None
    frame = None
    last_access = None

    camera = None
    rawCapture = None
    face_cascade = None

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def snapshot(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.framerate = 60

            # Load a cascade file for detecting faces
            dir = os.path.dirname(__file__)
            path = os.path.join(dir + '/lbpcascade_frontalface_improved.xml')
            if not os.path.isfile(path):
                print("Cannot find cv2 xml " + path)
            face_cascade = cv2.CascadeClassifier(path)

            rawCapture = PiRGBArray(camera, size=(320, 240))

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            # Capture frames from the camera
            for data in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

                image = data.array

                # Use the cascade file we loaded to detect faces
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray)

                print("Found " + str(len(faces)) + " face(s) " + str(threading.currentThread().ident))

                # Draw a rectangle around every face and move the motor towards the face
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 1)
                    # cv2.putText(image, "Face No." + str(len(faces)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # cv2.imshow( "Frame", image )
                #cv2.waitKey(1)

                # Clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                # encode ndarray
                result, encodedImage = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

                # store frame
                cls.frame = encodedImage.tostring()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 5:
                    break
        cls.thread = None

