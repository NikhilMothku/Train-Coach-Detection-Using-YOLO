import cv2
import os
import re

# Direct video path
VIDEO_PATH = "Raw_video/Full_Train_Split_Labelled.mp4"
OUTPUT_DIR = "OPTIMAL_COACH_FRAMES"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_train_coach_from_filename(filename):
    """
    Extract train and coach numbers from filename like Train1_Coach2.mp4
    Returns (train_number, coach_number)
    """
    match = re.search(r"[Tt]rain(\d+).*_[Cc]oach(\d+)", filename)
    if match:
        return match.group(1), match.group(2)
    else:
        return "UnknownTrain", "UnknownCoach"

def extract_frames(video_path, save_path, train_number, coach_number, num_frames=17):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        print(f"[WARNING] Could not read frames from {video_path}")
        return

    # Get 17 evenly spaced frame indices
    frame_ids = [int(i * total_frames / (num_frames - 1)) for i in range(num_frames)]

    frame_counter = 1
    for fid in frame_ids:
        cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
        ret, frame = cap.read()
        if ret:
            file_name = f"Train{train_number}_Coach{coach_number}_{frame_counter}.jpg"
            save_path_full = os.path.join(save_path, file_name)
            cv2.imwrite(save_path_full, frame)
            print(f"[SAVED] {save_path_full}")
            frame_counter += 1
        else:
            print(f"[ERROR] Failed to capture frame {fid} from {video_path}")

    cap.release()

# Process the given video file
video_file = os.path.basename(VIDEO_PATH)
train_num, coach_num = parse_train_coach_from_filename(video_file)
extract_frames(VIDEO_PATH, OUTPUT_DIR, train_num, coach_num, num_frames=17)

print(f"[INFO] 17 frames extracted in {OUTPUT_DIR}")
