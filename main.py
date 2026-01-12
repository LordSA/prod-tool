import threading
import time
import os
import tkinter as tk
from tkinter import scrolledtext, Entry, messagebox

import thala
import file_ops

# SETTINGS
DEFAULT_SOURCE = r"C:\Users\shibi\Downloads" #my username is used please change with yours
DEFAULT_DEST = r"C:\Users\shibi\Documents"
CHECK_INTERVAL = 3600

class ButlerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Smart Butler")
        self.root.geometry("450x550")
        self.root.configure(bg="#202124")
        self.chat = scrolledtext.ScrolledText(root, bg="#303134", fg="white", font=("Segoe UI", 10))
        self.chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat.insert(tk.END, "Butler: System Online. Ready to clean.\n\n")
        self.chat.configure(state='disabled')

        self.entry = Entry(root, font=("Segoe UI", 12), bg="#3C4043", fg="white")
        self.entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.entry.bind("<Return>", self.handle_input)

        threading.Thread(target=self.background_monitor, daemon=True).start()

    def add_msg(self, sender, text):
        self.chat.configure(state='normal')
        self.chat.insert(tk.END, f"{sender}: {text}\n\n")
        self.chat.see(tk.END)
        self.chat.configure(state='disabled')

    def handle_input(self, event):
        text = self.entry.get()
        if not text: return
        self.entry.delete(0, tk.END)
        self.add_msg("You", text)
        
        threading.Thread(target=self.run_ai, args=(text,)).start()

    def run_ai(self, text):
        self.root.after(0, lambda: self.add_msg("Butler", "Thinking..."))
        
        plan = thala.get_ai_command(text, DEFAULT_SOURCE, DEFAULT_DEST)
        
        if "error" in plan:
            self.root.after(0, lambda: self.add_msg("System", "AI Error."))
            return

        self.root.after(0, lambda: self.add_msg("Butler", f"Plan: {plan.get('confirmation')}"))
        result = file_ops.execute_organization(plan, DEFAULT_DEST)
        self.root.after(0, lambda: self.add_msg("Butler", result))

    def background_monitor(self):
        while True:
            time.sleep(CHECK_INTERVAL)
            if os.path.exists(DEFAULT_SOURCE):
                self.root.after(0, self.trigger_popup)

    def trigger_popup(self):
        if messagebox.askyesno("Cleanup", "Found old files. Clean them?"):
            self.run_ai("Clean old files")

if __name__ == "__main__":
    root = tk.Tk()
    app = ButlerApp(root)
    root.mainloop()