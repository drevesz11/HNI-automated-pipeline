import os

dir_path = "/home/drevesz/Desktop/segmentation_may23/Images/"

for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".nii.gz") or file.endswith(".bvec") or file.endswith(".bval"):
            os.remove(os.path.join(root, file))
            print(f"Deleted file: {os.path.join(root, file)}")