import cv2
import os

# Load OpenCV's pre-trained Haar Cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ask for employee name to create a unique folder
employee_name = input("Enter the employee's name: ").strip()
employee_dir = f'dataset/employees/{employee_name}'

# Create a folder if it doesn't exist
if not os.path.exists(employee_dir):
    os.makedirs(employee_dir)
else:
    print(f"Directory already exists for {employee_name}. New images will be added.")

# Start capturing from webcam
cap = cv2.VideoCapture(0)
print("Capturing images. Press 'q' to quit.")

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = frame[y:y+h, x:x+w]
        img_path = f"{employee_dir}/{employee_name}_{count}.jpg"
        cv2.imwrite(img_path, face)

        # Display the frame with the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Face Capture', frame)

    # Stop capturing after 20 images or when 'q' is pressed
    if count >= 20 or cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Captured {count} images for {employee_name}.")
