import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import convert_tif_to_geojson

class MyHandler(FileSystemEventHandler):
    def __init__(self, read_dir, processed_dir,destination_main_dir):
        self.read_dir = read_dir
        self.processed_dir = processed_dir
        self.destination_main_dir = destination_main_dir

    def on_created(self, event):
        # Check if the event is for a file
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)

            # Generate a relative path for the file to preserve subdirectory structure in the processed directory
            relative_raw_data_file_path = os.path.relpath(file_path, self.read_dir)
            processed_raw_data_file_path = os.path.join(self.processed_dir, relative_raw_data_file_path)

            destination_geojson_file_path = os.path.join(self.destination_main_dir,relative_raw_data_file_path.replace(".tif",".jsonl"))

            # Ensure the subdirectory exists in the processed directory
            os.makedirs(os.path.dirname(processed_raw_data_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(destination_geojson_file_path), exist_ok=True)

            # Implement your logic for processing the file here
            print(f'File {file_name} has been detected and is being processed.')

            print("Calling the convert function : ")

            convert_tif_to_geojson.trasnform_tif_to_geojson(file_path,destination_geojson_file_path)

            # Move the file to the corresponding subdirectory in the processed directory
            shutil.move(file_path, processed_raw_data_file_path)
            print(f'File {file_name} has been moved to {processed_raw_data_file_path}')

if __name__ == "__main__":


    read_dir = 'raw_data'
    trasnformed_data_dir = 'geo_json_formatted_data'

    processed_files_dir = 'history_processed_data'

    # Make sure the processed directory exists
    if not os.path.exists(processed_files_dir):
        os.makedirs(processed_files_dir)

    event_handler = MyHandler(read_dir, processed_files_dir,trasnformed_data_dir)
    observer = Observer()
    observer.schedule(event_handler, read_dir, recursive=True)  # Set recursive to True
    observer.start()

    try:
        while True:
            # Run indefinitely
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
