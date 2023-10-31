import tkinter as tk
from tkinter import filedialog
import shutil
import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor
import os
import time
import threading

from utils import choose_file_or_folder
from utils import process_documents_in_parallel
from dashlabs import DocumentProcessor
from dashlabs import ColumnCleaning

# if __name__ == "__main__":
    # input_path = choose_file_or_folder()
    # print(f"Selected path: {input_path}")
    # if not input_path:
    #     print("No file or folder selected. Exiting...")
    # else:
    #     # Ensure the target folder exists
    #     target_folder = "forms_uploaded"
    #     os.makedirs(target_folder, exist_ok=True)

    #     if os.path.isfile(input_path):
    #         # If a single file is chosen, copy it to the target folder
    #         file_name = os.path.basename(input_path)
    #         target_path = os.path.join(target_folder, file_name)
    #         shutil.copy(input_path, target_path)
    #     elif os.path.isdir(input_path):
    #         # If a folder is chosen, copy all files (excluding .env) to the target folder
    #         for file_name in os.listdir(input_path):
    #             if file_name != ".env":
    #                 src_path = os.path.join(input_path, file_name)
    #                 dest_path = os.path.join(target_folder, file_name)
    #                 shutil.copy(src_path, dest_path)

    #     # Process documents in parallel
    #     process_documents_in_parallel(target_folder)

# Create a tkinter GUI
root = tk.Tk()
root.title("Document Processing Tool")

# Target folders
target_folder = "forms_uploaded"
processed_folder = "processed_forms"

# Function to process the selected file or folder
def process_documents(input_path):
    os.makedirs(target_folder, exist_ok=True)

    if os.path.isfile(input_path):
        # If a single file is chosen, copy it to the target folder
        file_name = os.path.basename(input_path)
        target_path = os.path.join(target_folder, file_name)
        shutil.copy(input_path, target_path)
    elif os.path.isdir(input_path):
        # If a folder is chosen, copy all files (excluding .env) to the target folder
        for file_name in os.listdir(input_path):
            if file_name != ".env":
                src_path = os.path.join(input_path, file_name)
                dest_path = os.path.join(target_folder, file_name)
                shutil.copy(src_path, dest_path)

    # Process documents in parallel
    process_documents_in_parallel(target_folder)
    move_processed_files(target_folder)

def move_processed_files(src_folder):
    os.makedirs(processed_folder, exist_ok=True)
    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)
        dest_path = os.path.join(processed_folder, filename)
        shutil.move(src_path, dest_path)

# Function to process a single file or folder
def process_file_or_folder(option):
    input_path = filedialog.askopenfilename() if option == "1" else filedialog.askdirectory()
    if input_path:
        processing_thread = threading.Thread(target=process_documents, args=(input_path,))
        processing_thread.start()

# Create buttons for processing a single file or a folder
process_file_button = tk.Button(root, text="Process a Single File", command=lambda: process_file_or_folder("1"))
process_folder_button = tk.Button(root, text="Process a Folder", command=lambda: process_file_or_folder("2"))
process_file_button.pack()
process_folder_button.pack()

# Function to generate CSV files for download
def generate_csv_files():
    for filename in os.listdir(processed_folder):
        if filename.endswith(".json"):
            json_folder = os.path.join(processed_folder, filename)
            combiner = ColumnCleaning(json_folder, processed_folder)
            column_order = combiner.get_column_order()
            combiner.combine_json_to_csv(column_order)

generate_csv_button = tk.Button(root, text="Generate CSV Files", command=generate_csv_files)
generate_csv_button.pack()

# Function to list and download the generated CSV files
def list_and_download_csv_files():
    csv_files = [filename for filename in os.listdir(processed_folder) if filename.endswith(".csv")]
    for filename in csv_files:
        download_button = tk.Button(root, text=f"Download {filename}", command=lambda filename=filename: download_csv(filename))
        download_button.pack()

def download_csv(filename):
    csv_path = os.path.join(processed_folder, filename)
    os.system(f"start excel.exe {csv_path}")

list_and_download_button = tk.Button(root, text="List and Download CSV Files", command=list_and_download_csv_files)
list_and_download_button.pack()

# Start the tkinter main loop
root.mainloop()

###################################################################################################################################
# COLUMN CLEANING ## 

source_json_folder = 'output_json'
target_csv_folder = "output_csv_folder"

if os.path.exists(source_json_folder) and os.path.isdir(source_json_folder):
    folder_list = [folder for folder in os.listdir(source_json_folder) if os.path.isdir(os.path.join(source_json_folder, folder))]
    for folder in folder_list:
        
        if folder == "hiv_cert_json":
            personal_data = [
                'form name', 'certify name', 'physician', 'license number', 'date medical exam',
                'date', 'name', 'age', 'gender', 'civil status', 'address'
            ]
            results_and_other_details = [
                'screening test', 'result','technologist', 'hiv cert number', 'expiry date', 'pathologist'
            ]
            
            column_order = [*personal_data, *results_and_other_details]
        
        elif folder == "med_seafarers_cert_model":
            personal_data = [
                'form name', 'surname', 'first name', 'middle name', 'age', 'date of birth', 'place of birth',
                'nationality', 'gender', 'civil status', 'religion', 'address', 'passport number', 'seaman book number',
                'position', 'company']
            declarations = [
                'documents checked', 'hearing stwcode', 'unaided hearing', 'visual acuity', 'colour vision', 
                'date of last colour vision test', 'visual', 'lookout duties', 'restrictions', 'suffer med condition'
            ]
            other_details = [
                'exam given to', 'result', 'physician', 'date of exam', 'med director', 'issuing auth', 'address auth',
                'certifying auth', 'license number', 'seaferer signature', 'signature date', 'date of issuance', 'date of expiry'
            ]
            column_order = [*personal_data, *declarations, *other_details]
            
        elif folder == "med_landbase_exam_json":
            personal_data = [
                "form name","last name","first name","middle name","age","date of birth","place of birth",
                "nationality","gender", "civil status","religion","address","passport number",
                "destination","position", "company"
            ]
            medical_history = [
                "head injury", "frequent headache", "frequent diziness", "neurological disorder",
                "sleep disorder", "mental disorder", "eye problem","ear disorder", "nose or throat disorder",
                "tuberculosis", "lung disorder", "high blood pressure", "heart disease", "rheumatic",
                "diabetes","endocrine disorder", "cancer or tumor", "blood disorder", "stomach pain",
                "abdominal disorder", "gynaecological disorder", "bladder disorder", "back or joint injury",
                "familial disorder", "sexually transmitted disease", "tropical disease", "schistosomiasis",
                "asthma", "allergies", "operation/s", "signed of as sick", "hospitalized", "declared unfit for work overseas",
                "medical cert been restricted", "aware to any medical problem", "feel fit", "allergic medication", 
                "taking medication"
            ]
            medical_exam = [
                "height","weight","blood pressure","pulse rate","rhythm","respiration","bmi",
                "far vision uncorrected", "far vision corrected", "near vision uncorrected",
                "near vision corrected", "isahara color vision", "hearing right ear", "hearing left ear",
                "clarity speech", "skin", "head neck scalp", "eyes external", "pupils", "ears", 
                "nose sinus", "mouth throat", "neck", "chest", "lungs", "heart", "abdomen", "back",
                "anus rectum",  "genito urinary system", "inguinals genitals", "extremities", "reflexes",
                "dental",
            ]
            results = [
                "xray", "ecg", "cbc", "urinalysis", "stool", "hepa", "hiv test", "rpr", "blood type",
                "psychological test", "additional test"
            ]
            summary = [
                "basic doh med exam", "additional test", "host med lab", "result"
            ]
            other_details = [
                "date med exam", "date med expire", "med exam report number", "physician", "license number",
                "clinic address", "clinic name", "date sign"
            ]
            
            column_order = [*personal_data, *medical_history, *medical_exam, *results, *summary, *other_details]
        
        combiner = ColumnCleaning(folder, target_csv_folder) 
        combiner.combine_json_to_csv(column_order)