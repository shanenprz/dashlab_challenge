from concurrent.futures import ThreadPoolExecutor
from dashlabs import DocumentProcessor
import os
from .time_it import time_it

@time_it
def process_documents_in_parallel(input_folder):
    # Get a list of files in the input folder
    file_list = os.listdir(input_folder)

    with ThreadPoolExecutor(max_workers=5) as executor:
        for file_name in file_list:
            if os.path.isfile(os.path.join(input_folder, file_name)):
                doc_processor = DocumentProcessor()
                executor.submit(doc_processor.process_single_document, os.path.join(input_folder, file_name), file_name)