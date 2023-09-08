import os

dir_path = "/home/drevesz/Desktop/segmentation_may23/Images/"

for root, dirs, files in os.walk(dir_path):
    # Check if any of the directories have the specified names
    for directory in dirs:
        if directory == "b0" or directory == "DWI":
            directory_path = os.path.join(root, directory)
            # Check if the directory is empty
            if not os.listdir(directory_path):
                os.rmdir(directory_path)
                print(f"Deleted empty directory: {directory_path}")