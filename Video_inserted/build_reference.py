# import cv2
# import mediapipe as mp
# import numpy as np
# import json
# import os
# import sys

# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()

# KEY_POINTS = [11,12,13,14,15,16]

# # cap = cv2.VideoCapture("Videos\Greetings.mp4")
# video_path = sys.argv[1]
# action_name = sys.argv[2]

# cap = cv2.VideoCapture(video_path)

# print("Video path:", video_path)
# print("Exists:", os.path.exists(video_path))


# if not cap.isOpened():
#     print(" Video not opened")
#     exit()

# ref_data = []

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print(" No frame read")
#         break
#     print("Frame read")  # للتجربة

#     image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = pose.process(image)

#     if results.pose_landmarks:
#         print(" Pose detected")
#         lm = results.pose_landmarks.landmark

#         frame_data = []
#         for i in KEY_POINTS:
#             p = lm[i]
#             frame_data.append([p.x, p.y, p.z])

#         ref_data.append(frame_data)
#     else:
#        print(" No pose")

# cap.release()

# # action_name = input("Enter action name: ")

# with open(f"data/{action_name}.json", "w") as f:
#     json.dump(ref_data, f)

# print("Reference saved")





try:
    import cv2
    import mediapipe as mp
    import json
    import sys

    video_path = sys.argv[1]

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    cap = cv2.VideoCapture(video_path)

    all_frames = []

    if not cap.isOpened():
        print(json.dumps({"error": "Cannot open video"}))
        exit()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)

        if results.pose_landmarks:
            frame_data = []
            for lm in results.pose_landmarks.landmark:
                frame_data.append([lm.x, lm.y, lm.z])

            all_frames.append(frame_data)

    cap.release()

    # 🔥 لو مفيش بيانات
    if len(all_frames) == 0:
        print(json.dumps({"error": "No landmarks detected"}))
    else:
        print(json.dumps(all_frames))

except Exception as e:
    import json
    print(json.dumps({"error": str(e)}))