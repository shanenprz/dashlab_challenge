import tkinter as tk
from tkinter import filedialog
import os
from dashlabs.document_processor import DocumentProcessor

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        process_file(file_path)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_folder(folder_path)

def process_file(file_path):
    doc_processor = DocumentProcessor()
    doc_processor.process_single_document(file_path, os.path.basename(file_path))

def process_folder(folder_path):
    doc_processor = DocumentProcessor()
    doc_processor.output_folder = "output_json"  # Change the output folder if needed
    doc_processor.process_documents_in_parallel(folder_path)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    print("Select an option:")
    print("1: Upload a FILE")
    print("2: Upload a FOLDER")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        select_file()
    elif choice == "2":
        select_folder()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
