import face_recognition
import cv2
import numpy as np
import pickle
from datetime import datetime
import os
import pandas as pd

# Load the saved face encodings
with open('encodings.pkl', 'rb') as f:
    data = pickle.load(f)

known_encodings = data['encodings']
known_names = data['names']

# Create a folder for logs if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Today's log file path
log_file = f'logs/entry_log_{datetime.now().date()}.csv'

# Load existing logs to prevent duplicate entries
if os.path.exists(log_file):
    existing_logs = pd.read_csv(log_file)
    recognized_employees = set(existing_logs['Name'].tolist())
else:
    recognized_employees = set()

# Initialize webcam
cap = cv2.VideoCapture(0)
print("Starting real-time face recognition...")

detected = False  # Flag to check if recognition or duplicate detection occurs

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and encode them
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]

            if name not in recognized_employees:
                recognized_employees.add(name)
                entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Log entry time to CSV
                log_data = pd.DataFrame([[name, entry_time]], columns=["Name", "Entry Time"])
                if os.path.exists(log_file):
                    log_data.to_csv(log_file, mode='a', header=False, index=False)
                else:
                    log_data.to_csv(log_file, index=False)

                print(f"{name} recognized and marked present at {entry_time}.")
            else:
                print(f"{name} has already been marked present today.")

            detected = True  # Stop camera after recognition or duplicate detection

            # Display recognized face with name
            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            # Unknown face detected
            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Display the video feed
    cv2.imshow('Employee Entry Recognition', frame)

    # Exit loop if someone is recognized OR already marked OR 'q' is pressed
    if detected or cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close window
cap.release()
cv2.destroyAllWindows()
print("Real-time recognition stopped.")
