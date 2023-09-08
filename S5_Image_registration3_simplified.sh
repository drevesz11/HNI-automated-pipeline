#!/bin/bash

# Input directory
inputdir="/home/drevesz/Desktop/segmentation_may23/Images"

# Output directory
outputdir="/home/drevesz/Desktop/segmentation_may23/standardised_images_HNI_space/images"

# MRI template
template="/home/drevesz/Desktop/segmentation_may23/standardised_images_HNI_space/MRI-template.nii.gz"

# Loop through input files
for inputfile in $(find "$inputdir" -name "*_DWI.nii.gz"); do
  echo "Processing $inputfile"

  # Get output file names
  inputfilename=$(basename "$inputfile")
  outdir=$(dirname "$inputfile" | sed "s|$inputdir|$outputdir|")
  outfile="$outdir/$(basename "$inputfile" _DWI.nii.gz)_reg.nii.gz"
  outfile_mask="$outdir/$(basename "$inputfile" _DWI.nii.gz)_reg_mask.nii.gz"
  outfileWarp="$outdir/$(basename "$inputfile" _DWI.nii.gz)_Warp.nii.gz"
  outfile_reg="$outdir/$(basename "$inputfile" _DWI.nii.gz)_reg"
  
  # Create output directory if it does not exist
  mkdir -p "$outdir"

  # Registration
  ANTS 3 -m CC[$template,$inputfile,1,4] -o $outfile_reg

  if [[ $convergence == *0* ]]; then
    # Apply affine transform
    WarpImageMultiTransform 3 $inputfile $outfileWarp -R $template ${outfile_reg}Affine.txt
  else
    # Apply deformation field
    WarpImageMultiTransform 3 $inputfile $outfileWarp -R $template ${outfile_reg}Warp.nii.gz ${outfile_reg}Affine.txt
  fi

  echo "Registration done for subject $(basename "$inputfile")"
done
 
echo "All done"