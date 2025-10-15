import cv2
import os

def load_faces_labels(data_path='data/faces'):
    faces = []
    labels = []
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
    return faces, labels