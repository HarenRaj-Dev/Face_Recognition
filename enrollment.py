import cv2
import os

dataset_path = 'data/faces/'

if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

def run_enrollment(face_id):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            img_name = f"User.{face_id}.{count}.jpg"
            cv2.imwrite(os.path.join(dataset_path, img_name), gray[y:y+h, x:x+w])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            count += 1
        cv2.imshow('Enrollment', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 100:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Finished collecting {count} face samples for UserID {face_id}")

# Remove prompt for input — handled via GUI dialog, not here!