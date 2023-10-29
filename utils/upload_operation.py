import tkinter as tk
from tkinter import filedialog
import shutil
from .time_it import time_it

@time_it
def choose_file_or_folder():
    root = tk.Tk()
    root.withdraw()
    option = input("Choose an option (1: Upload a File, 2: Upload a Folder): ")
    input_path = ""
    if option == "1":
        input_path = filedialog.askopenfilename()  # Open a file dialog to choose a file
    elif option == "2":
        input_path = filedialog.askdirectory()  # Open a dialog to choose a folder
    root.destroy()  # Close the main window
    return input_path