import os

# Set the main directory path
main_dir = "/home/drevesz/Desktop/segmentation_may23/Images"

# Loop through all subdirectories within the main directory
for subdir, dirs, files in os.walk(main_dir):
    # Loop through all files in the current subdirectory
    for file in files:
        # Check if the file contains '.dcm' in its filename
        if '.dcm' in file:
            # Construct the full path of the file and delete it
            file_path = os.path.join(subdir, file)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
