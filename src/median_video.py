import cv2
import numpy as np
from scipy.stats import mode

def compute_median_frame(input_video_path, output_image_path):
    """
    Reads a video file frame-by-frame, computes the median of all frames
    (per pixel, across time), and saves the resulting image.
    
    Args:
        input_video_path  (str): Path to the input video file.
        output_image_path (str): Path to save the median image.
    """

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Cannot open video file: {input_video_path}")
        return

    frames = []

    # --- Read all frames into a Python list ---
    while True:
        ret, frame = cap.read()
        if not ret:
            # No more frames or can't read the frame
            break
        frames.append(frame)

    cap.release()
    
    if not frames:
        print("No frames found in the video!")
        return

    # Convert the list of frames (H x W x C) into a NumPy array: (N x H x W x C)
    #   where N = number of frames
    frames_array = np.stack(frames, axis=0)

    # Compute the median across the time dimension (N)
    #   Result shape: (H, W, C)
    print(f"Median frame shape: 5")
    median_frame = mode(frames_array, axis=0, keepdims=False)[0]

    # Convert from float to uint8 so we can save it as an image
    #   Median might not be an integer; np.median returns float by default
    print(f"Median frame shape: {median_frame.shape}")
    median_frame = median_frame.astype(np.uint8)
    print(f"Median frame data type: {median_frame.dtype}")

    # --- Save the resulting median frame ---
    cv2.imwrite(output_image_path, median_frame)
    print(f"Median frame saved to: {output_image_path}")


if __name__ == "__main__":
    input_video = "/Users/emin/Desktop/ee475/piano-transcription/dataset/MIDItest/miditest_videos/25.mp4"
    output_image = "/Users/emin/Desktop/ee475/piano-transcription/dataset/MIDItest/miditest_videos/no_hand_frames/25/mode.jpg"
    compute_median_frame(input_video, output_image)