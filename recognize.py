import cv2
import numpy as np
import os
from datetime import datetime
import pandas as pd

def run_attendance():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []
    data_path = 'data/faces/'

    for img_name in os.listdir(data_path):
        if img_name.startswith('User') and img_name.endswith('.jpg'):
            parts = img_name.split('.')
            if len(parts) == 4 and parts[1].isdigit() and parts[2].isdigit():
                label = int(parts[1])
                img_path = os.path.join(data_path, img_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    faces.append(img)
                    labels.append(label)

    if len(faces) == 0:
        print("No training data found. Run enrollment first.")
        return

    recognizer.train(faces, np.array(labels))

    attendance_path = 'attendance.csv'
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        df = pd.read_csv(attendance_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Date', 'UserID'])

    THRESHOLD = 70
    marked_today = set(map(int, df[df['Date'] == today]['UserID']))

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces_detected:
            roi_gray = gray[y:y + h, x:x + w]
            user_id, confidence = recognizer.predict(roi_gray)
            if confidence < THRESHOLD:
                color = (0, 255, 0) if user_id not in marked_today else (0, 0, 255)
                text = f"ID: {user_id} ({round(confidence, 1)})"
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                if user_id not in marked_today:
                    df = pd.concat([df, pd.DataFrame([{'Date': today, 'UserID': user_id}])], ignore_index=True)
                    df.to_csv(attendance_path, index=False)
                    marked_today = set(map(int, df[df['Date'] == today]['UserID']))
            else:
                color = (0, 255, 255)
                text = "Unknown"
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow('Recognition & Attendance', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()