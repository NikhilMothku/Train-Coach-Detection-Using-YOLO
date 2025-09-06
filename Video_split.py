import cv2
import os
from ultralytics import YOLO


RAW_VIDEO = "Raw_video/Coach_count_using_YOLO.mp4"
OUTPUT_DIR = "COACH_SPLIT_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)


model = YOLO("yolov8n.pt") 

def split_video(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps

   
    segment_length = 10 
    frames_per_segment = int(fps * segment_length)

    num_coaches = int(duration_sec // segment_length)

    print(f"[INFO] Video has {duration_sec:.2f}s, FPS={fps}, Coaches={num_coaches}")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    coach_counter = 1
    frame_counter = 0
    out = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

       
        if frame_counter % frames_per_segment == 0:
            if out:
                out.release()

            folder_name = f"Coach_{coach_counter}"
            save_dir = os.path.join(output_dir, folder_name)
            os.makedirs(save_dir, exist_ok=True)

            h, w, _ = frame.shape
            out = cv2.VideoWriter(
                os.path.join(save_dir, f"{folder_name}.mp4"),
                fourcc, fps, (w, h)
            )

            print(f"[INFO] Started {folder_name}")
            coach_counter += 1

        if out:
            out.write(frame)

        frame_counter += 1

    cap.release()
    if out:
        out.release()
    print(f"[INFO] All coach videos saved in {OUTPUT_DIR}")

split_video(RAW_VIDEO, OUTPUT_DIR)
