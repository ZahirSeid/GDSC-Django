import os
import shutil
from datetime import datetime, timedelta

def list_files_in_directory(directory="."):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def is_file_updated_last_24_hours(file_path):
    try:
        file_stats = os.stat(file_path)
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        
        # Check if either creation time or modification time is within the last 24 hours
        return datetime.fromtimestamp(file_stats.st_ctime) > twenty_four_hours_ago or \
               datetime.fromtimestamp(file_stats.st_mtime) > twenty_four_hours_ago
    except Exception as e:
        print(f"Error checking file {file_path}: {e}")
        return False

def update_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Append a timestamp to the content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_content = f"{content}\nUpdated at: {timestamp}"
        
        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)
    except Exception as e:
        print(f"Error updating file {file_path}: {e}")

def create_last_24hours_folder(folder_name="last_24hours"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def move_file_to_folder(file_path, folder_name="last_24hours"):
    try:
        destination_path = os.path.join(folder_name, os.path.basename(file_path))
        shutil.move(file_path, destination_path)
        print(f"Moved {file_path} to {destination_path}")
    except Exception as e:
        print(f"Error moving file {file_path}: {e}")

def main():
    current_directory = os.getcwd()
    create_last_24hours_folder()

    files_in_directory = list_files_in_directory(current_directory)

    for file_name in files_in_directory:
        file_path = os.path.join(current_directory, file_name)

        if is_file_updated_last_24_hours(file_path):
            update_file(file_path)
            move_file_to_folder(file_path)

if __name__ == "__main__":
    main()

