import os
import shutil
import time
import json
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, messagebox
import google.generativeai as genai

API_KEY = "AIzaSyDAodPnTZPB411VH6QUmX0IhalQTd2qcGo" #your gemini key

DEFAULT_SOURCE = r"C:\Users\shibi\Downloads" # use your user name to it
DEFAULT_DEST_ROOT = r"C:\Users\shibi\Documents"

CHECK_INTERVAL_SECONDS = 3600
FILE_AGE_THRESHOLD_HOURS = 24

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def get_ai_command(user_text):
    prompt = f"""
    You are a file organization assistant. Interpret the user's request and output a JSON object.
    
    Current Default Source: {DEFAULT_SOURCE}
    Current Default Root Destination: {DEFAULT_DEST_ROOT}

    User Request: "{user_text}"

    Output JSON with these keys:
    1. "source_folder": (string) Full path. If not specified, use Default Source.
    2. "destination_folder_name": (string) The name of the subfolder to create/use (e.g., "Invoices", "Images"). Infer this from context.
    3. "file_extensions": (list of strings) e.g., [".pdf", ".docx"]. If "all", return ["*"]. If "images", return [".jpg", ".png", ".webp"].
    4. "time_filter_hours": (int) Only move files older than this. If user says "old", use 24. If "all" or "now", use 0.
    5. "confirmation": (string) A short, friendly summary of what you are doing.

    Output ONLY JSON. No markdown.
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": str(e)}

def execute_organization(command_json):
    source = command_json.get("source_folder", DEFAULT_SOURCE)
    subfolder = command_json.get("destination_folder_name", "Sorted_Files")
    extensions = command_json.get("file_extensions", ["*"])
    age_hours = command_json.get("time_filter_hours", 0)
    
    dest_path = os.path.join(DEFAULT_DEST_ROOT, subfolder)
    
    if not os.path.exists(source):
        return f"Error: Source folder {source} does not exist."
    
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    moved_count = 0
    current_time = time.time()

    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            if "*" not in extensions and file_ext not in extensions:
                continue
            
            file_age = (current_time - os.path.getmtime(file_path)) / 3600
            if file_age < age_hours:
                continue

            try:
                shutil.move(file_path, os.path.join(dest_path, filename))
                moved_count += 1
            except Exception as e:
                print(f"Skipped {filename}: {e}")

    return f"Success! Moved {moved_count} files to '{subfolder}' folder."

def background_checker(app):
    while True:
        time.sleep(CHECK_INTERVAL_SECONDS)
        
        count = 0
        current_time = time.time()
        if os.path.exists(DEFAULT_SOURCE):
            for f in os.listdir(DEFAULT_SOURCE):
                fp = os.path.join(DEFAULT_SOURCE, f)
                if os.path.isfile(fp):
                    age = (current_time - os.path.getmtime(fp)) / 3600
                    if age > FILE_AGE_THRESHOLD_HOURS:
                        count += 1
        
        if count > 0:
            app.root.after(0, lambda: app.show_notification(count))

class SmartButlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Smart Butler")
        self.root.geometry("450x550")
        self.root.configure(bg="#202124")

        self.chat = scrolledtext.ScrolledText(root, bg="#303134", fg="white", font=("Segoe UI", 10), wrap=tk.WORD)
        self.chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat.insert(tk.END, "Butler: I'm listening. You can say:\n- 'Move all PDFs to a Work folder'\n- 'Clean up old images'\n- 'Sort everything from Downloads'\n\n")
        self.chat.configure(state='disabled')

        self.entry = Entry(root, font=("Segoe UI", 12), bg="#3C4043", fg="white", insertbackground="white")
        self.entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.handle_input)

        self.monitor_thread = threading.Thread(target=background_checker, args=(self,), daemon=True)
        self.monitor_thread.start()

    def add_msg(self, sender, text):
        self.chat.configure(state='normal')
        self.chat.insert(tk.END, f"{sender}: {text}\n\n")
        self.chat.see(tk.END)
        self.chat.configure(state='disabled')

    def handle_input(self, event):
        user_text = self.entry.get()
        if not user_text: return
        self.entry.delete(0, tk.END)
        
        self.add_msg("You", user_text)
        self.add_msg("Butler", "Thinking...")
        
        threading.Thread(target=self.process_command, args=(user_text,)).start()

    def process_command(self, text):
        command_json = get_ai_command(text)
        
        if "error" in command_json:
            self.root.after(0, lambda: self.add_msg("Butler", "Error connecting to AI."))
            return

        self.root.after(0, lambda: self.add_msg("Butler", f"Plan: {command_json.get('confirmation')}"))
        
        result = execute_organization(command_json)
        self.root.after(0, lambda: self.add_msg("Butler", result))

    def show_notification(self, count):
        response = messagebox.askyesno("Clutter Alert", f"I found {count} old files in Downloads.\nShould I clean them up automatically?")
        if response:
            self.add_msg("System", "User authorized auto-clean via popup.")
            self.process_command("Clean up all old files from downloads")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartButlerApp(root)
    root.mainloop()