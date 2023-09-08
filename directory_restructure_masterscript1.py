#Part 1 - remove the more recent scan (only want the acute image)
import os
import shutil
from datetime import datetime

def remove_recent_scan(dir_path): 
    """
    Remove the more recent scan directory from the subject directory if there are 2 directories.
    """
    sub_dirs = [os.path.join(dir_path, d) for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
    scan_dirs = [d for d in sub_dirs if len(os.listdir(d)) == 1]  # Scans have only one subdirectory
    if len(scan_dirs) != 2:
        return  # There aren't two scans in this subject directory
    dates = [datetime.strptime(os.path.basename(d), '%Y-%m-%d') for d in scan_dirs]
    newer_dir = scan_dirs[0] if dates[0] > dates[1] else scan_dirs[1]
    shutil.rmtree(newer_dir)

for dirpath, dirnames, filenames in os.walk('.'):
    for dirname in dirnames:
        remove_recent_scan(os.path.join(dirpath, dirname))


#Part 2 - relabels the Diffusion folder to the format SubjectID where ID is the number in the directory 
# Path to the base directory
base_path = '/home/drevesz/Desktop/segmentation_may23/Images'

# Loop through each directory in the base directory
for dirpath, dirnames, filenames in os.walk(base_path):
    # Check if the current directory is a 'Diffusion' directory
    if os.path.basename(dirpath) == 'Diffusion':
        # Get the parent directory name (the subject ID)
        parent_dirname = os.path.basename(os.path.dirname(os.path.dirname(dirpath)))
        # Rename the 'Diffusion' directory to the format 'SUBJECTID_FOLDER'
        new_dirname = f'Subject{parent_dirname}'
        try:
            os.rename(dirpath, os.path.join(os.path.dirname(dirpath), new_dirname))
            # Print the old and new directory names
            print(f'Renamed {os.path.basename(dirpath)} to {new_dirname}')
        except PermissionError:
            print(f'Could not rename {os.path.basename(dirpath)} due to a permission error')


#Part 4 - Simplify directory structure - Cuts out the subjectID directory (containing b0 and DWI folders and images) into the desired main directory location  
import shutil

# Set the source directory to the home directory
src_dir = '/home/drevesz/Desktop/segmentation_may23/Images'

# Set the destination directory
dst_dir = '/home/drevesz/Desktop/segmentation_may23/Images'

# Loop through all directories in the source directory
for root, dirs, files in os.walk(src_dir):
    for dir in dirs:
        # Check if the directory name contains 'Subject'
        if 'Subject' in dir:
            # Create the destination directory with the same name as the source directory
            dst_subdir = os.path.join(dst_dir, dir)
            os.makedirs(dst_subdir, exist_ok=True)
            # Loop through all files in the source directory and move them to the destination directory
            for file in os.listdir(os.path.join(root, dir)):
                shutil.move(os.path.join(root, dir, file), os.path.join(dst_subdir, file))
            # Remove the original directory
            shutil.rmtree(os.path.join(root, dir))

# Remove the original source directory
shutil.rmtree(src_dir)

