# needed imports
import cv2
import mediapipe as mp


def points_track(x1, y1, x2, y2):  # function to find the orientation
    if x1 - x2 not in range(-25, 25):
        if x1 < x2:
            print("left")
        else:
            print("right")
    else:
        if y1 > y2:
            print("up")
        else:
            print("down")


cap = cv2.VideoCapture(0)  # start filming video

# needed to draw points
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# need empty dictionary for saving current point locations
pointDict = {}

while True:
    # detect hands
    ret, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # drawing lines
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # find point locations
            for ids, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # put point locations in dictionary
                pointDict[ids] = (cx, cy)

            # use tracking function for the index finger points
            points_track(pointDict[6][0], pointDict[6][1], pointDict[8][0], pointDict[8][1])

            # closes program if middle finger is shown
            if pointDict[10][1] > pointDict[12][1] and pointDict[6][1] < pointDict[8][1]:
                if pointDict[14][1] < pointDict[16][1] and pointDict[9][1] > pointDict[10][1] :
                    print("stop")
                    cap.release()
                    cv2.destroyAllWindows()
            # put points on screen/ not nessesary just looks cool
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # print flipped image
    cv2.imshow("Image", cv2.flip(img, 1))

    # close tab with q
    if cv2.waitKey(1) == ord('q'):
        break

# release cam
cap.release()
cv2.destroyAllWindows()
