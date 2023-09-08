import os
import subprocess

# Set the base directory to search
base_dir = "/home/drevesz/Desktop/segmentation_may23/Images"

# Set the path to the ADSRun.py script
ads_script = "/home/drevesz/Desktop/segmentation_may23/scripts/ADSv1.2/codes/ADSRun.py"

# Loop through all subdirectories
for root, dirs, files in os.walk(base_dir):
    for dir in dirs:
        # Get the full path to the subdirectory
        subdir_path = os.path.join(root, dir)
        # Construct the command to run ADSRun.py on the subdirectory
        cmd = f"python {ads_script} -input {subdir_path}"
        # Use subprocess to execute the command
        subprocess.run(cmd, shell=True)