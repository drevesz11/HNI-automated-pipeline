#!/bin/bash

# Input directory
input_dir="/home/drevesz/Desktop/segmentation_may23/Images"

# Registration inputs directory
registration_dir="/home/drevesz/Desktop/segmentation_may23/standardised_images_HNI_space/images"

# Output directory
output_dir="/home/drevesz/Desktop/segmentation_may23/standardised_images_HNI_space/images"

# Template image
template_image="/home/drevesz/Desktop/segmentation_may23/standardised_images_HNI_space/MRI-template.nii.gz"

# Loop through subdirectories
for subdir in "$input_dir"/*; do
  if [ -d "$subdir" ]; then
    # Get the subject ID from the subdirectory name
    subject_id=$(basename "$subdir" | sed 's/Subject//')

    # Get the corresponding registration inputs directory
    registration_subdir="$registration_dir/Subject${subject_id}"

    # Loop through files in the subdirectory
    for file in "$subdir"/*_Predict.nii.gz; do
      if [ -f "$file" ]; then
        # Get the filename without the directory path
        filename=$(basename "$file")

        # Generate the output file name
        output_file="$output_dir/Subject${subject_id}/${filename%_Predict.nii.gz}_lesion_registered.nii.gz"

        # Get the paths to the registration files
        affine_file="$registration_subdir/Subject${subject_id}_regAffine.txt"
        warp_file="$registration_subdir/Subject${subject_id}_regWarp.nii.gz"

        # Create the output directory if it doesn't exist
        mkdir -p "$(dirname "$output_file")"

        # Print the input and output file paths
        echo "Input file: $file"
        echo "Output file: $output_file"

        # Execute the registration command
        WarpImageMultiTransform 3 "$file" "$output_file" -R "$template_image" "$warp_file" "$affine_file" --use-NN
      fi
    done
  fi
done

