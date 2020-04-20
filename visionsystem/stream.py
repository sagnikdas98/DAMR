import cv2
import os
import acapture
import threading

import rtsp

cap = cv2.VideoCapture("rtsp://admin:111111@10.25.117.102:10554/tcp/av0_0")
cap.set(cv2.CAP_PROP_FOURCC,  cv2.VideoWriter.fourcc('H','2','6','4'))
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
# cap = cv2.VideoCapture(0)


if cap.isOpened()== False:
    print("Error camera 1 isn't connecting")


while (cap.isOpened()):
    ret, img = cap.read()
    if ret == True:
        cv2.imshow('Video 1',img)

    else:
        print('wtf')

    if cv2.waitKey(1) and 0xFF == ord('q'):
        break



# cap = acapture.open("rtsp://admin:111111@10.25.117.102:10554/tcp/av0_0", frame_capture=True)
# while True:
#     check,frame = cap.read() # non-blocking
#     if check:
#         frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#         cv2.imshow("test",frame)
#         cv2.waitKey(1)


# with rtsp.Client(rtsp_server_uri = 'rtsp://admin:111111@10.25.117.102:10554/tcp/av0_0') as client:
#     client.preview()

    

# def captureimages():
#     while True:
#         cap.grab()

# s = threading.Thread(target=captureimages)
# s.start()

# while (cap.isOpened()):
#     img = cap.retrieve()
#     cv2.imshow('Video 1',img)

# cap = cv2.VideoCapture("rtsp://admin:111111@10.25.117.102:10554/tcp/av0_0.h264")

# while(1):

#     ret, frame = cap.read()
#     cv2.imshow('VIDEO', frame)
#     cv2.waitKey(1)
# ffmpeg -rtsp_transport tcp -i rtsp://10.25.117.102:10554/tcp/av0_0 -f image2 -vf fps=fps=1 hello/img%03d.png
# ffplay rtsp://admin:111111@10.25.117.102:10554/tcp/av0_0

# cap.release()
# cv2.destroyAllWindows()

# ffmpeg -rtsp_transport tcp -i rtsp://admin:111111@10.25.117.102:10554/tcp/av0_0 -f image2 -vf fps=fps=1 hello/img%03d.png
