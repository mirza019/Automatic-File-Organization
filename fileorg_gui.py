import os
import shutil
import time
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from datetime import datetime, timedelta, time as dt_time
import json

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("400x400") # Increased geometry to ensure developer name visibility

        self.UNDO_LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fileorg_undo_log.json")

        # --- Developer Name (packed first to ensure it's at the bottom) ---
        self.developer_label = tk.Label(self, text="Developed by Mirza Shaheen Iqubal", font=("Arial", 8))
        self.developer_label.pack(side=tk.BOTTOM, pady=(0, 5))

        # --- Main Container (packed above the developer label) ---
        container = tk.Frame(self, padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=tk.YES)

        # --- Organize Button ---
        self.organize_button = tk.Button(container, text="Organize Today's Files", command=self.organize_today)
        self.organize_button.pack(fill=tk.X, pady=10)

        # --- Undo Button ---
        self.undo_button = tk.Button(container, text="Undo Last Organization", command=self.undo_last_organization)
        self.undo_button.pack(fill=tk.X, pady=10)

        # --- Progress Bar ---
        self.progress = ttk.Progressbar(container, length=100)
        self.progress.pack(fill=tk.X, pady=5)

        # --- Output Log ---
        self.output_text = scrolledtext.ScrolledText(container, wrap=tk.WORD, height=8, relief="solid", borderwidth=1)
        self.output_text.pack(fill=tk.BOTH, expand=tk.YES) # Allow output_text to expand within its container

        self.update_undo_button_state()

    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.update_idletasks()

    def update_undo_button_state(self):
        if os.path.exists(self.UNDO_LOG_FILE):
            self.undo_button.config(state=tk.NORMAL)
        else:
            self.undo_button.config(state=tk.DISABLED)

    def organize_today(self):
        self.output_text.delete(1.0, tk.END)
        self.log("Organizing files created today...")
        today_start = datetime.combine(datetime.now().date(), dt_time.min).timestamp()
        self.organize_files(lambda t: t >= today_start)

    def organize_files(self, time_filter):
        source_folder = os.path.dirname(os.path.abspath(__file__))
        destination_map = {
            "Documents": [".txt", ".pdf", ".doc", ".docx"],
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Videos": [".mp4", ".mov", ".avi"],
            "Music": [".mp3", ".wav"],
            "Archives": [".zip", ".rar", ".7z"],
            "Installers": [".dmg", ".pkg"],
            "Applications": [".app"],
        }

        for folder in destination_map.keys():
            if not os.path.exists(os.path.join(source_folder, folder)):
                os.makedirs(os.path.join(source_folder, folder))

        files_to_move = []
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            if filename in [os.path.basename(__file__), "fileorg.py", os.path.basename(self.UNDO_LOG_FILE)]:
                continue
            try:
                creation_time = os.path.getctime(file_path)
            except OSError:
                continue
            if time_filter(creation_time):
                files_to_move.append((filename, file_path))

        self.progress['maximum'] = len(files_to_move)
        moved_files_log = []
        for i, (filename, file_path) in enumerate(files_to_move):
            self.progress['value'] = i + 1
            self.update_idletasks()
            original_path = file_path
            new_path = ""
            moved = False

            if filename.endswith(".app") and os.path.isdir(file_path):
                new_path = os.path.join(source_folder, "Applications", filename)
                shutil.move(file_path, new_path)
                self.log(f"Moved {filename} to Applications.")
                moved = True
            elif os.path.isdir(file_path):
                continue
            else:
                _, file_extension = os.path.splitext(filename)
                file_extension = file_extension.lower()
                for folder, extensions in destination_map.items():
                    if file_extension in extensions:
                        new_path = os.path.join(source_folder, folder, filename)
                        shutil.move(file_path, new_path)
                        self.log(f"Moved {filename} to {folder}.")
                        moved = True
                        break
            
            if not moved and not os.path.isdir(file_path):
                others_folder = os.path.join(source_folder, "Others")
                if not os.path.exists(others_folder):
                    os.makedirs(others_folder)
                new_path = os.path.join(others_folder, filename)
                shutil.move(file_path, new_path)
                self.log(f"Moved {filename} to Others.")
                moved = True
            
            if moved:
                moved_files_log.append({"source": original_path, "destination": new_path})

        if moved_files_log:
            with open(self.UNDO_LOG_FILE, "w") as f:
                json.dump(moved_files_log, f, indent=4)
            messagebox.showinfo("Success", f"File organization complete. Moved {len(moved_files_log)} files.")
        else:
            messagebox.showinfo("Complete", "No files matched the criteria to organize.")
        
        self.progress['value'] = 0
        self.update_undo_button_state()

    def undo_last_organization(self):
        if not os.path.exists(self.UNDO_LOG_FILE):
            messagebox.showerror("Error", "No undo information found.")
            return

        with open(self.UNDO_LOG_FILE, "r") as f:
            moves = json.load(f)

        self.progress['maximum'] = len(moves)
        undone_count = 0
        for i, move in enumerate(reversed(moves)):
            self.progress['value'] = i + 1
            try:
                shutil.move(move["destination"], move["source"])
                self.log(f"Moved back: {os.path.basename(move['source'])}")
                undone_count += 1
            except Exception as e:
                self.log(f"Error undoing {os.path.basename(move['destination'])}: {e}")

        try:
            os.remove(self.UNDO_LOG_FILE)
        except OSError as e:
            self.log(f"Error removing undo log: {e}")

        self.log(f"\nUndo complete. Restored {undone_count} files.")
        messagebox.showinfo("Undo Complete", f"Restored {undone_count} files.")
        self.progress['value'] = 0
        self.update_undo_button_state()

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()