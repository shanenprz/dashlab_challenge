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
from dashlabs import JsonToCsvCombiner

# Define the target folders and output folder
target_folders = [
    "hiv_cert",
    "med_exam_landbase",
    "med_cert_landbase",
    "med_cert_seafarers",
]
output_csv_folder = "output_csv"

document_processor = DocumentProcessor()
document_processor.process_and_save_documents()

# Create an instance of the class and call the method
combiner = JsonToCsvCombiner(target_folders, output_csv_folder)
combiner.combine_json_to_csv()
