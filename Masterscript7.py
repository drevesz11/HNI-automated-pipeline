import pydicom
import os
import subprocess

#Part 1 - Rename DICOM files to .dcm
# Set the path to the directory containing the DICOM files
dir_path = "/home/drevesz/Desktop/segmentation_may23/Images"

# Loop through all subdirectories
for subdir, dirs, files in os.walk(dir_path):
    # Loop through all files in the subdirectory
    for filename in files:
        # Check if it's a DICOM file
        if not filename.endswith(".dcm"):
            # Check if it's a file in a Diffusion folder
            if "Diffusion" in subdir:
                try:
                    # Rename the file to include the .dcm ending
                    os.rename(os.path.join(subdir, filename), os.path.join(subdir, filename + ".dcm"))
                except OSError:
                    print(f"Skipping file {filename} in {subdir} as it cannot be renamed")


#Part 2 - b0 and dwi renaming based on header metadata  
# Set the path to the parent directory containing the subdirectories with DICOM files
parent_dir = "/home/drevesz/Desktop/segmentation_may23/Images"

# Create empty lists to hold the directories containing 0 b0 or dwi files
dirs_with_0_b0_files = []
dirs_with_0_dwi_files = []

# Loop through all subdirectories within the parent directory
for subdir, dirs, files in os.walk(parent_dir):
    # Check if the current subdirectory contains 'Diffusion' in its path
    if 'Diffusion' not in subdir:
        continue

    print("Searching directory:", subdir)

    # Create empty lists to hold the b0, dwi, and unclassified files
    b0_files = []
    dwi_files = []
    unclassified_files = []

    # Loop through all files in the subdirectory
    for filename in files:
        print("Parsing file name:", filename)
        # Check that the file is a DICOM file and has SequenceName attribute
        if filename.endswith(".dcm") and hasattr(pydicom.read_file(os.path.join(subdir, filename), force=True), 'SequenceName'):
            # Load the DICOM file
            dcm = pydicom.read_file(os.path.join(subdir, filename), force=True)

            # Check if it's a b0 file based on the tags and metadata
            if ("b0" in dcm.SequenceName.lower() if hasattr(dcm, 'SequenceName') else False or 
                (hasattr(dcm, "DiffusionDirectionality") and 
                 dcm.DiffusionDirectionality == "NONE") or 
                (hasattr(dcm, "ProtocolName") and 
                 "b0" in dcm.ProtocolName.lower()) or
                (hasattr(dcm, "MRDiffusionSequence") and
                 dcm.MRDiffusionSequence[0].DiffusionGradientDirectionSequence[0].bvalue == 0) or
                (hasattr(dcm, "ImagingFrequency") and 
                 dcm.ImagingFrequency == 0)):
                if "b0" in dcm.SequenceName.lower(): # Recognize SequenceName containing 'b0'
                    b0_files.append(filename)
            elif 'b0' not in filename and 'dwi' not in filename:
                print("Renaming", os.path.join(subdir, filename), "to", os.path.join(subdir, "dwi_" + filename))
                os.rename(os.path.join(subdir, filename), os.path.join(subdir, "dwi_" + filename))

    # Rename the b0 files to include the b0 label
    for filename in b0_files:
        print("Renaming", os.path.join(subdir, filename), "to", os.path.join(subdir, "b0_" + filename))
        os.rename(os.path.join(subdir, filename), os.path.join(subdir, "b0_" + filename))

    # Rename the dwi files to include the dwi files to include the dwi label
    for filename in dwi_files:
        print("Renaming", os.path.join(subdir, filename), "to", os.path.join(subdir, "dwi_" + filename))
        os.rename(os.path.join(subdir, filename), os.path.join(subdir, "dwi_" + filename))

    # Check if the subdirectory contains only unclassified files and rename to dwi
    if b0_files and unclassified_files:
        for filename in unclassified_files:
            if filename.endswith('.dcm'):
                print("Renaming", os.path.join(subdir, filename), "to", os.path.join(subdir, "dwi_" + filename))
                os.rename(os.path.join(subdir, filename), os.path.join(subdir, "dwi_" + filename))

    
#Part 3 - Split the b0 and dwi DICOM files into 2 folders 
# Loop through all subdirectories within the parent directory
for subdir, dirs, files in os.walk(parent_dir):
    # Check if the current subdirectory contains 'Diffusion' in its path
    if 'Diffusion' not in subdir:
        continue

    # Create the 'b0' and 'DWI' directories if they don't exist
    b0_dir = os.path.join(subdir, 'b0')
    dwi_dir = os.path.join(subdir, 'DWI')
    os.makedirs(b0_dir, exist_ok=True)
    os.makedirs(dwi_dir, exist_ok=True)

    # Move the b0 and dwi files to their respective directories
    for filename in os.listdir(subdir):
        if filename.startswith('b0_'):
            os.rename(os.path.join(subdir, filename), os.path.join(b0_dir, filename))
        elif filename.startswith('dwi_'):
            os.rename(os.path.join(subdir, filename), os.path.join(dwi_dir, filename))

#Part 4 - Convert labelled b0 and dwi files into nifty files using dcm2niixloop2 
# Loop through all subdirectories within the parent directory
for subdir, dirs, files in os.walk(parent_dir):
    # Check if the current subdirectory contains 'Diffusion' in its path
    if 'Diffusion' not in subdir:
        continue

    # Loop through the b0 and dwi folders within the subdirectory
    for folder in ['b0', 'DWI']:
        folder_path = os.path.join(subdir, folder)
        if os.path.isdir(folder_path):
            print("Found", folder, "folder:", folder_path)

            # Create a list to hold the DICOM files
            dicom_files = []

            # Loop through all files in the folder
            for filename in os.listdir(folder_path):
                # Check that the file is a DICOM file
                if filename.endswith(".dcm"):
                    dicom_files.append(os.path.join(folder_path, filename))

            # Convert and combine the DICOM files
            if len(dicom_files) > 0:
                print("Combining", len(dicom_files), folder, "files into one NIfTI image...")
                output_file = os.path.join(subdir, folder + ".nii.gz")
                subprocess.run(["dcm2niix", "-o", subdir, "-f", folder, "-z", "y", "-m", "y", *dicom_files])

print("Done!")
