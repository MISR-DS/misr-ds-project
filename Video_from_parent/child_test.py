import cv2
import mediapipe as mp
import numpy as np
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

child_data = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        landmarks = results.pose_landmarks.landmark

        frame_data = []
        for lm in landmarks:
            frame_data.append([lm.x, lm.y, lm.z])

        child_data.append(frame_data)

    cv2.imshow("Child Gesture", image)

    # اقفلي بالكليك Q
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# حفظ حركة الطفل
with open("child_gesture.json", "w") as f:
    json.dump(child_data, f)

print("Child gesture saved!")