import cv2 as cv
import numpy as np

video_path = r'C:\Users\mahmo\.vscode\video_process\pre_process\video1\What Does High-Quality Preschool Look Like  NPR Ed.mp4'
capture = cv.VideoCapture(video_path)

if not capture.isOpened():
    print("Error: Could not open video.")
    exit()


output_size = (640, 640)
processed_frames = []

frame_count = 0


while True:
    ret, frame = capture.read()
    
    # Break the loop if no more frames are available
    if not ret:
        break
    
    # Sample every 5th frame
    if frame_count % 5 == 0:
        # Resize frame
        resized_frame = cv.resize(frame, output_size, interpolation=cv.INTER_LINEAR)
        
        # Normalizing pixel values
        normalized_frame = resized_frame / 255.0
        
        normalized_frame = normalized_frame.astype(np.float32)

        rgb_frame = cv.cvtColor(normalized_frame, cv.COLOR_BGR2RGB)
        
        processed_frames.append(rgb_frame)
    
    frame_count += 1

capture.release()

frames_array = np.array(processed_frames)

np.save('processed_frames4.npy', frames_array)

print("Finished processing video. Total sampled frames:", len(processed_frames))