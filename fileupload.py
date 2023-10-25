import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def process_upload(upload_path, target_folder):
    upload_path = Path(upload_path)
    if upload_path.is_file() and not upload_path.name.endswith(".env"):
        destination_path = Path(target_folder) / upload_path.name
        shutil.copy(upload_path, destination_path)
        messagebox.showinfo("File Uploaded", f"File '{upload_path.name}' copied to '{target_folder}'")
    elif upload_path.is_dir():
        for file in upload_path.iterdir():
            if file.name != '.env':
                destination_path = Path(target_folder) / file.name
                shutil.copy(file, destination_path)
                messagebox.showinfo("File Uploaded", f"File '{file.name}' copied to '{target_folder}'")
    else:
        messagebox.showerror("Invalid Path", "Invalid path. Please provide a valid file or folder.")

def browse_folder_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    upload_folder = filedialog.askopenfilename(title="Select the file or folder to upload")
    target_folder = filedialog.askdirectory(title="Select the target folder")
    root.destroy()
    return upload_folder, target_folder
