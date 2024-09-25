import cv2
from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)  # Track only one hand

while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img)

    # Check if at least one hand is detected
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 landmarks points
        indexFingerTip = lmList[8] # Index finger tip (landmark 8)
        thumbTip = lmList[4]  # Thumb tip (landmark 4)

        # Print the coordinates of the index finger tip
        print(f"Index Finger Coordinates: x={indexFingerTip[0]}, y={indexFingerTip[1]}")
        print(f"Thumb Finger Coordinates: x={thumbTip[0]}, y={indexFingerTip[1]}")


    # Display the image with detected hands
    cv2.imshow("Hand Tracking", img)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
