import cv2 as cv

cap = cv.VideoCapture("rtsp://admin:admin123@192.168.0.127:554/Streaming/Channels/101")
cap1 = cv.VideoCapture("rtsp://admin:admin123@192.168.0.127:554/Streaming/Channels/401")

if cap.isOpened()== False:
    print("Error camera 1 isn't connecting")
if cap1.isOpened()== False:
    print("Error camera 2 isn't connecting")

while (cap.isOpened() or cap1.isOpened()):
   ret, img = cap.read()
   ret1, img1 = cap1.read()
   if ret == True:
       cv.imshow('Video 1',img)
       cv.imshow('Video 2',img1)

   if cv.waitKey(1) and 0xFF == ord('q'):
        break

cap.release()
cap1.release()
cv.destroyAllWindows()
