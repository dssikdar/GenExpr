import os
import re
import shutil

# Define the parent directory where the STDS0000XXX directories are located
parent_dir = '/extra/zhanglab0/dsikdar/'

# Define the regex pattern for matching the directories
pattern = re.compile(r'^STDS0000\d{3}$')

# Traverse the parent directory
for root, dirs, files in os.walk(parent_dir):
    for dir_name in dirs:
        if pattern.match(dir_name):
            print(f"\nDirectory: {dir_name}")
            dir_path = os.path.join(root, dir_name)
            print("REMOVED: ")
            for file_name in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file_name)

                # Check if it is a directory and remove it recursively
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"\t• {file_path} (directory)")
                else:
                    # Remove files that do not match the criteria
                    if not (file_name.endswith('_processed.h5ad') or
                            file_name.endswith('.png') or
                            file_name.endswith('.jpg')):
                        os.remove(file_path)
                        print(f"\t• {file_path}")

            # Remove the main directory if empty
            if not os.listdir(dir_path) and input("Delete? ") == "y":
                os.rmdir(dir_path)
                print(f"\t• {dir_path} (empty directory removed)")
           
