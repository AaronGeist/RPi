from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2


class Camera:
    camera = None
    rawCapture = None
    face_cascade = None

    def __init__(self):
        # Setup the camera
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 60
        self.rawCapture = PiRGBArray(self.camera, size=(320, 240))

        # Load a cascade file for detecting faces
        self.face_cascade = cv2.CascadeClassifier('./lbpcascade_frontalface.xml')

    def snapshot(self):
        # Capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):

            image = frame.array

            # Use the cascade file we loaded to detect faces
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray)

            print("Found " + str(len(faces)) + " face(s)")

            # Draw a rectangle around every face and move the motor towards the face
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 1)
                # cv2.putText(image, "Face No." + str(len(faces)), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # cv2.imshow( "Frame", image )
            cv2.waitKey(1)

            # Clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # encode ndarray
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 98]
            result, encodedImage = cv2.imencode('.jpg', image, encode_param)

            return encodedImage.tostring()

