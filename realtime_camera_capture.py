import cv2

cap = cv2.VideoCapture(0)

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
        cv2.imshow("Webcam Live", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
