# import cv2
# import sys

# action_name = sys.argv[1]
# cap = cv2.VideoCapture(0)
# video_path = f"videos/{action_name}.mp4"

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # out = cv2.VideoWriter('Videos/new_action.mp4', fourcc, 20.0, (640,480))
# out = cv2.VideoWriter(f'Videos/{action_name}.mp4', fourcc, 20.0, (640,480))

# print("Recording... press q to stop")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     out.write(frame)
#     cv2.imshow('Recording', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# out.release()
# cv2.destroyAllWindows()

# print("Video saved")


##########################

# import cv2
# import sys

# action = sys.argv[1]

# cap = cv2.VideoCapture(0)

# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter(f'videos/{action}.mp4', fourcc, 20.0, (640, 480))

# print("START_RECORDING")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     out.write(frame)

#     cv2.imshow("Recording... Press Q to stop", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# out.release()
# cv2.destroyAllWindows()

# print("DONE")

import cv2
import sys
import time


action = sys.argv[1]

cap = cv2.VideoCapture(0)
cv2.namedWindow("Recording", cv2.WINDOW_NORMAL)

cv2.setWindowProperty(
    "Recording",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)

cv2.setWindowProperty(
    "Recording",
    cv2.WND_PROP_TOPMOST,
    1
)

out = cv2.VideoWriter(
    f"videos/{action}.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    20.0,
    (640, 480)
)
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)

    cv2.imshow("Recording", frame)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.waitKey(1)
    if  time.time() - start_time >= 15:
        break

cap.release()
out.release()
cv2.destroyAllWindows()