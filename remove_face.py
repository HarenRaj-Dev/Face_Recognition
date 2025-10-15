import os

def remove_user_faces(user_id, folder='data/faces/'):
    count = 0
    for fname in os.listdir(folder):
        parts = fname.split('.')
        if len(parts) == 4 and parts[1].isdigit() and int(parts[1]) == user_id:
            os.remove(os.path.join(folder, fname))
            count += 1
    print(f"Removed {count} images for UserID {user_id}")
    return count  # Now returns count for the GUI

def run_remove_user(user_id):
    return remove_user_faces(user_id)