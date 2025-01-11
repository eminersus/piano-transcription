import cv2
import mediapipe as mp
import os
import csv

def process_video(
    input_video_path, 
    no_hand_frames_dir="no_hand_frames", 
    fingertip_csv_path="fingertips.csv"
):
    """
    1. Read a video from 'input_video_path'.
    2. For each frame:
       - If no hand is detected, save the frame in 'no_hand_frames_dir'.
       - If a hand is detected, extract (x, y) of fingertip landmarks (indices [4,8,12,16,20]) 
         and append them to 'fingertips.csv'.
    3. Log every 100 frames processed.
    4. Do not display frames during processing (no cv2.imshow).
    5. Close the file at the end.
    """

    # --- Setup: create output directory and CSV file ---
    if not os.path.exists(no_hand_frames_dir):
        os.makedirs(no_hand_frames_dir)

    # Open the CSV file in write mode (overwrite if it already exists)
    # Columns: frame_index, hand_index, fingertip_id, x, y
    with open(fingertip_csv_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["frame_index", "hand_index", "fingertip_id", "x", "y"])

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,   # We are processing a video
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # Open the video capture
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Cannot open video file: {input_video_path}")
        return

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video file reached or cannot read the frame.")
            break

        # Convert BGR to RGB before processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Check if hands are detected
        if not results.multi_hand_landmarks:
            # NO hand: save the frame
            no_hand_frame_path = os.path.join(
                no_hand_frames_dir, 
                f"frame_{frame_index:06d}.jpg"
            )
            cv2.imwrite(no_hand_frame_path, frame)
        else:
            # If there are hands, extract fingertip coordinates
            image_height, image_width, _ = frame.shape

            # Append fingertip data to CSV
            with open(fingertip_csv_path, mode='a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)

                for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Fingertip indices in MediaPipe Hands
                    fingertip_ids = [4, 8, 12, 16, 20]
                    for tip_id in fingertip_ids:
                        # Calculate pixel coordinates
                        x = hand_landmarks.landmark[tip_id].x * image_width
                        y = hand_landmarks.landmark[tip_id].y * image_height
                        csv_writer.writerow([frame_index, hand_idx, tip_id, x, y])

        # Log every 100 frames
        if (frame_index + 1) % 100 == 0:
            print(f"Processed up to frame {frame_index + 1}")

        frame_index += 1

    # Release resources
    cap.release()
    print("Processing complete.")
    print(f"No-hand frames saved to: {no_hand_frames_dir}")
    print(f"Fingertips saved in: {fingertip_csv_path}")

# Example usage:
if __name__ == "__main__":
    videos = [5, 10, 21, 23, 24, 25, 26, 27]
    for video in videos:
        input_video = f"dataset/MIDItest/miditest_videos/{video}.mp4"
        process_video(
            input_video_path=input_video,
            no_hand_frames_dir=f"dataset/MIDItest/miditest_videos/no_hand_frames/{video}",
            fingertip_csv_path=f"dataset/MIDItest/miditest_videos/fingertips/{video}.csv"
        )
        print(f"video {video} done")
