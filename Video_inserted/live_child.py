import cv2
import mediapipe as mp
import json
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cv2.namedWindow("Child Live", cv2.WINDOW_NORMAL)

cv2.setWindowProperty(
     "Child Live",
      cv2.WND_PROP_FULLSCREEN,
      cv2.WINDOW_FULLSCREEN
    )

cv2.setWindowProperty(
      "Child Live",
      cv2.WND_PROP_TOPMOST,
      1
    )

child_data = []

start_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        # mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        lm = results.pose_landmarks.landmark

        frame_data = []
        # for i in [11,12,13,14,15,16]:
        #     p = lm[i]
        #     frame_data.append([p.x, p.y, p.z])
        for lm in results.pose_landmarks.landmark:
            frame_data.append([lm.x, lm.y, lm.z])

        child_data.append(frame_data)


    # cv2.namedWindow("Child Live", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty(
    #   "Child Live",
    #    cv2.WND_PROP_FULLSCREEN,
    #    cv2.WINDOW_FULLSCREEN
      
    # )
   

    cv2.imshow("Child Live", image)

    # if cv2.waitKey(10) & 0xFF == ord('q'):
    cv2.waitKey(1)
    if  time.time() - start_time >= 15:
        break

cap.release()
cv2.destroyAllWindows()

with open("child.json", "w") as f:
    json.dump(child_data, f)

print("Child saved")