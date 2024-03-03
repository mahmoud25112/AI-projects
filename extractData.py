import pandas as pd
import cv2
import numpy as np
import ast
import keras
from keras import layers

def extract_object(frame_array, bbox, target_size=(256, 256)):
    x_min, y_min, x_max, y_max = [int(coord) for coord in bbox]
    if x_min >= 0 and y_min >= 0 and x_max <= frame_array.shape[1] and y_max <= frame_array.shape[0]:
        object_img = frame_array[y_min:y_max, x_min:x_max]
        object_img_resized = cv2.resize(object_img, target_size, interpolation=cv2.INTER_AREA)
        return object_img_resized
    else:
        return None

# Load CSV data
csv_path = 'detection_resultsHot.csv'
try:
    data = pd.read_csv(csv_path)
    data['bbox info'] = data['bbox info'].apply(ast.literal_eval)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

# Load preprocessed frames
try:
    frames_array = np.load('processed_framesGroof.npy')
except Exception as e:
    print(f"Error loading Numpy file: {e}")
    exit(1)

preprocessed_objects = []
sampling_rate = 5

for index, row in data.iterrows():
    frame_num = row['frameNum']
    correct_index = (frame_num - 1) // sampling_rate

    if correct_index < len(frames_array):
        frame_array = frames_array[correct_index]
        bbox = row['bbox info']
        object_img = extract_object(frame_array, bbox)
        if object_img is not None:
            preprocessed_objects.append(object_img)

preprocessed_objects_array = np.array(preprocessed_objects)
np.save('preprocessed_objectsGroof.npy', preprocessed_objects_array)
