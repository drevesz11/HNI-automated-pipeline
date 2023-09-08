import os
import glob
import nibabel as nib

# Set the root directory to start searching from
root_dir = '/home/drevesz/Desktop/segmentation_may23/Images'

# Loop through all directories and subdirectories from the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Loop through all files in the current directory
    for filename in filenames:
        # Check if the filename matches the pattern "Subject*_DWI.nii.gz"
        if filename.startswith("Subject") and filename.endswith("_DWI.nii.gz"):
            # Construct the full path to the NIfTI file
            file_path = os.path.join(dirpath, filename)
            
            # Load the NIfTI file using nibabel
            nifti_img = nib.load(file_path)
            
            # Get the current shape of the NIfTI data
            current_shape = nifti_img.shape
            
            # Check if the NIfTI data is 4D
            if len(current_shape) == 4:
                # Reshape the NIfTI data to remove the fourth dimension
                new_shape = current_shape[:-1]
                nifti_data = nifti_img.get_fdata()[:,:,:,0]
                
                # Create a new NIfTI image with the reshaped data
                nifti_img_3D = nib.Nifti1Image(nifti_data, nifti_img.affine, nifti_img.header)
                
                # Overwrite the original NIfTI image with the reshaped data
                nib.save(nifti_img_3D, file_path)
                
                # Do whatever you want with the new file here
                print(f"Reshaped file {file_path} and overwrote the original file")


