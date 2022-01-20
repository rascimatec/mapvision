import cv2

camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(2)

while(1):
    ret, frame = camera1.read()
    cv2.imshow("camera 1", frame)

    ret, frame = camera2.read()
    cv2.imshow("camera 2", frame)
   
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

captura.release()
cv2.destroyAllWindows()