import os
import shutil

source_dir = "/home/drevesz/Desktop/AXIS-2-2016-copy/Final-trial-images-Jan-23"
target_dir = "/home/drevesz/Desktop/segmentation_may23/Images"

total_dirs = sum([len(dirs) for r, dirs, files in os.walk(source_dir) if "Diffusion" in r])

count = 0
for root, dirs, files in os.walk(source_dir):
    for directory in dirs:
        if "Diffusion" in directory:
            count += 1
            source_path = os.path.join(root, directory)
            relative_path = os.path.relpath(source_path, source_dir)
            target_path = os.path.join(target_dir, relative_path)
            shutil.copytree(source_path, target_path, copy_function=shutil.copy2)
            print(f"Copied directory {count}/{total_dirs}: {source_path} -> {target_path}")