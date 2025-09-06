import cv2
import os
from ultralytics import YOLO


INPUT_VIDEO = "Raw_video/Train_Video.mp4"
OUTPUT_DIR = "Coach_Splits_By_Detection"
os.makedirs(OUTPUT_DIR, exist_ok=True)


model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(INPUT_VIDEO)
fps = int(cap.get(cv2.CAP_PROP_FPS))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

coach_index = 1
out = None
frames_written = 0
split_length = fps * 10  

while True:
    ret, frame = cap.read()
    if not ret:
        break

  
    results = model(frame)
    boxes = results[0].boxes

    
    detected_train = False
    for box in boxes:
        cls_id = int(box.cls[0])
        label = results[0].names[cls_id]
        if label.lower() == "train":   
            detected_train = True
            break

    if detected_train:
        if out is None:  
            video_path = os.path.join(OUTPUT_DIR, f"Coach_{coach_index}.mp4")
            out = cv2.VideoWriter(video_path, fourcc, fps, (w, h))
            frames_written = 0
            print(f"[INFO] Started Coach_{coach_index}")

        
        cv2.putText(frame, f"Coach {coach_index}", (40, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)

        out.write(frame)
        frames_written += 1

        
        if frames_written >= split_length:
            out.release()
            print(f"[INFO] Saved Coach_{coach_index}")
            coach_index += 1
            out = None


if out:
    out.release()
cap.release()

print(f"[INFO] Completed! {coach_index-1} coaches saved in {OUTPUT_DIR}")
