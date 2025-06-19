import os
import shutil

# Define the source folder to organize
source_folder = os.path.dirname(os.path.abspath(__file__))


# Define destination folders based on file extensions
destination_map = {
    "Documents": [".txt", ".pdf", ".doc", ".docx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
    "Installers": [".dmg", ".pkg"],
    "Applications": [".app"],  # .app is treated as a folder
}

# Ensure destination folders exist
for folder in destination_map.keys():
    destination_path = os.path.join(source_folder, folder)
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

# Sort files and special application folders
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)

    # Skip this script itself
    if filename == os.path.basename(__file__):
        continue
        
    # Get the file extension
    _, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower()

    moved = False

    # Check if it's a .app bundle (directory)
    if filename.endswith(".app") and os.path.isdir(file_path):
        destination = os.path.join(source_folder, "Applications", filename)
        shutil.move(file_path, destination)
        print(f"Moved application bundle {filename} to Applications folder.")
        continue

    # Skip other directories
    if os.path.isdir(file_path):
        continue

    # Move regular files to the appropriate folder
    for folder, extensions in destination_map.items():
        if file_extension in extensions:
            shutil.move(file_path, os.path.join(source_folder, folder, filename))
            print(f"Moved {filename} to {folder} folder.")
            moved = True
            break

    # If the file type doesn't match, move to "Others"
    if not moved:
        others_folder = os.path.join(source_folder, "Others")
        if not os.path.exists(others_folder):
            os.makedirs(others_folder)
        shutil.move(file_path, os.path.join(others_folder, filename))
        print(f"Moved {filename} to Others folder.")

print("File organization complete.")
