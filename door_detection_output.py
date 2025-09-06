import cv2
from ultralytics import YOLO

INPUT_VIDEO = "Raw_video/Raw_Video.mp4"
OUTPUT_VIDEO = "door_detection_output.mp4"

model = YOLO("DOOR_DETECTION")  # Pretrained YOLO for door detection

cap = cv2.VideoCapture(INPUT_VIDEO)
fps = int(cap.get(cv2.CAP_PROP_FPS))
w = int(cap.get(3))
h = int(cap.get(4))

out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    annotated = results[0].plot()
    out.write(annotated)

cap.release()
out.release()
print(f"[INFO] Door detection output saved: {OUTPUT_VIDEO}")
