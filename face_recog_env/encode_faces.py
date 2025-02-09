import face_recognition
import os
import cv2
import numpy as np
import pickle

# Path to the dataset folder where employee images are stored
dataset_dir = 'dataset/employees'
encodings = []
employee_names = []

# Loop through each employee's folder
for employee in os.listdir(dataset_dir):
    employee_path = os.path.join(dataset_dir, employee)

    # Loop through each image of the employee
    for img_name in os.listdir(employee_path):
        img_path = os.path.join(employee_path, img_name)
        image = face_recognition.load_image_file(img_path)
        face_locations = face_recognition.face_locations(image)

        # Ensure there's exactly one face in the image
        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(image)[0]
            encodings.append(face_encoding)
            employee_names.append(employee)
        else:
            print(f"Skipping {img_path}: Found {len(face_locations)} faces.")

# Save the encodings and corresponding employee names to a file
with open('encodings.pkl', 'wb') as f:
    pickle.dump({'encodings': encodings, 'names': employee_names}, f)

print(f"Encoded {len(encodings)} images. Data saved to encodings.pkl.")
