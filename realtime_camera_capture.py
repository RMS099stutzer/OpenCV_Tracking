import cv2
import numpy as np

cap = cv2.VideoCapture(0)

lower = np.array([0,0,0])
upper = np.array([255,255,100])

disable = False

if cap.isOpened() == False:
    print("❌ Cannot open camera")
    exit()

if cap.isOpened():
    print("✅ VideoCapture is opened!")
    print("Width: " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("Height: " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("FPS: " + str(cap.get(cv2.CAP_PROP_FPS)))
          
    print("Press 'q' to quit")


while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        if not disable:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame_mask = cv2.inRange(hsv, lower, upper)

            frame = cv2.bitwise_and(frame, frame, mask=frame_mask)
        
        cv2.imshow("Webcam Live", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
