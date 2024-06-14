import os
import csv
import requests

def download_file(url, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad requests
        file_name = url.split('/')[-1]
        with open(os.path.join(directory, file_name), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {file_name} into {directory}")
    except requests.RequestException as e:
        print(f"Failed to download {url}. Reason: {e}")

def process_csv(file_path, dataset_id):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['download']
            if url.endswith('.h5ad') or url.endswith('hires_image.png') or url.endswith('hires_image.jpg') or \
               url.endswith('.jpg.gz') or url.endswith('images.tar.gz') or url.endswith('spatial.tar.gz'):
                download_file(url, dataset_id)
        os.remove(file_path)
        
def main():
    csv_directory = 'datainfo'
    if not os.path.isdir(csv_directory):
        print(f"Error: Directory {csv_directory} does not exist.")
        return

    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_directory, filename)
            dataset_id = filename.split('_')[1].split('.')[0]
            print(f"\nProcessing file: {file_path}")
            process_csv(file_path, dataset_id)
            

    print("\nAll downloads completed.")

if __name__ == "__main__":
    main()

