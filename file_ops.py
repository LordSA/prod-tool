import os
import shutil
import time
import winsound 
# from playsound import playsound # Use this for Mac/Linux

def play_success_sound():
    try:
        winsound.Beep(1000, 200) 
        # For Mac/Linux using playsound:
        # playsound('success.mp3') 
    except:
        pass

def execute_organization(command_json, default_root):
    source = command_json.get("source_folder")
    subfolder = command_json.get("destination_folder_name", "Sorted")
    extensions = command_json.get("file_extensions", ["*"])
    age_hours = command_json.get("time_filter_hours", 0)
    
    dest_path = os.path.join(default_root, subfolder)
    
    if not os.path.exists(source):
        return f"Error: Source {source} not found."
    
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    count = 0
    current_time = time.time()

    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if "*" not in extensions and ext not in extensions:
                continue
            file_age = (current_time - os.path.getmtime(file_path)) / 3600
            if file_age < age_hours:
                continue

            try:
                shutil.move(file_path, os.path.join(dest_path, filename))
                count += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")

    if count > 0:
        play_success_sound()
        return f"Success! Moved {count} files to {subfolder}."
    else:
        return "No matching files found to move."