import os
import tarfile
import gzip
import shutil

def delete_subfolders(directory):
    """Recursively delete all subfolders in the given directory."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted subfolder: {item_path}")

# Define the path to the main directory containing all the "STDS0000XXX" folders
main_directory = '/extra/zhanglab0/dsikdar'

# List all directories in the main directory
directories = [d for d in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, d)) and d.startswith('STDS0000')]

# Process each directory
for directory in directories:
    dir_path = os.path.join(main_directory, directory)
    # List all files in the directory
    files = os.listdir(dir_path)

    for file in files:
        # Create full file path for downloading file
        file_path = os.path.join(dir_path, file)

        # Check if the file is a tar.gz file
        if file.endswith('.tar.gz'):
            print(f"Directory: {directory}")
            print(f"File: {file}") 
            
            # Obtain name of tar_gz file for identification
            tar_gz_name = os.path.splitext(os.path.splitext(file)[0])[0]

            try:
                with tarfile.open(file_path, 'r:gz') as tar:
                    # Extract only the files containing "hires" in the filename
                    for member in tar.getmembers():
                        if 'hires' in member.name:
                            # Manually extract to avoid subdirectories
                            member.name = os.path.basename(member.name)
                            tar.extract(member, path=dir_path)

                            # Append the tar.gz file name to the extracted file's name
                            extracted_file_path = os.path.join(dir_path, member.name)
                            new_file_name = f"{tar_gz_name}_{member.name}"
                            new_file_path = os.path.join(dir_path, new_file_name)
                            os.rename(extracted_file_path, new_file_path)
                            print(f'Renamed {member.name} to {new_file_name}')

            except Exception as e:
                print(f"ERROR in .tar.gz file: {e}")

        # Check if the file is a gzipped file (but not tar.gz)
        '''
        if file.endswith('.png.gz') or file.endswith('.jpg.gz') and not file.endswith('.tar.gz'):
            print(f"File: {file}")
            if 'hires' in file:
                with gzip.open(file_path, 'rb') as f_in:
                    # Create a decompressed output file path, stripping .gz
                    output_file_path = os.path.join(dir_path, file[:-3])
                    with open(output_file_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(f"{output_file_path} done")
        '''

    # After processing all files in the directory, delete any subfolders
    #delete_subfolders(dir_path)

print("Extraction complete.")

