#!/usr/bin/env python3
import cv2
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands


tipIds = [4, 8, 12, 16, 20]

video = cv2.VideoCapture(0)

hands = mp_hand.Hands(max_num_hands=1)

while True:
    ret, image = video.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    lmList = []
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            myHands = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
           
                lmList.append([id, cx, cy])

            mp_draw.draw_landmarks(
                image, hand_landmark,
                mp_hand.HAND_CONNECTIONS)

    fingers = []
    if len(lmList) != 0:
       
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1) 
        else:
            fingers.append(0)  

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)  
            else:
                fingers.append(0) 

        total = fingers.count(1)

        if total == 0:
            print("Emergency help")
            cv2.putText(image, "Emergency help", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)


        elif total == 5:
            print("Medication help")
            cv2.putText(image, "Medication help", (45, 375),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

    
  
    imS = cv2.resize(image, (960, 720))                   
    cv2.imshow("Gesture detection", imS)     

  

    k = cv2.waitKey(1)
    
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
