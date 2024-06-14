import os
import csv
import requests

def download_file(url, directory):
    # Ensure the target directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_name = url.split('/')[-1]
    file_path = os.path.join(directory, file_name)
    
    # Skip download if file already exists
    if os.path.exists(file_path):
        print(f"File {file_name} already exists in {directory}. Skipping download.")
        return
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad requests
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {file_name} into {directory}")
    except requests.RequestException as e:
        print(f"Failed to download {url}. Reason: {e}")

def process_csv(file_path, directory):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['download']
            if url.endswith('.png.gz') or url.endswith('.jpg.gz'):
                download_file(url, directory)

def main():
    csv_directory = 'datainfo'
    if not os.path.isdir(csv_directory):
        print(f"Error: Directory {csv_directory} does not exist.")
        return

    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_directory, filename)
            # Assuming each CSV file's name relates to a dataset ID
            dataset_id = filename.split('.')[0]  # Customize this if needed
            print(f"\nProcessing file: {file_path}")
            process_csv(file_path, dataset_id)

    print("\nAll downloads completed.")

if __name__ == "__main__":
    main()

