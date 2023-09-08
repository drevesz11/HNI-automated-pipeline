import os

root_dir = '/home/drevesz/Desktop/segmentation_may23/Images'

for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the directory contains b0 and DWI files
    if 'b0.nii.gz' in filenames and 'DWI.nii.gz' in filenames:
        # Get the subject ID from the parent directory name
        subject_id = os.path.basename(dirpath)
        # Rename the b0 and DWI files
        os.rename(os.path.join(dirpath, 'b0.nii.gz'), os.path.join(dirpath, subject_id + '_b0.nii.gz'))
        os.rename(os.path.join(dirpath, 'DWI.nii.gz'), os.path.join(dirpath, subject_id + '_DWI.nii.gz'))