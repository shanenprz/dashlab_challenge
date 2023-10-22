from dashlabs import DocumentProcessor
from dashlabs import JsonToCsvCombiner

# Define the target folders and output folder
target_folders = [
    "hiv_cert",
    "med_exam_landbase",
    "med_cert_landbase",
    "med_cert_seafarers",
    "med_exam_seafarers"
]
output_csv_folder = "output_csv01"

# document_processor = DocumentProcessor()
# document_processor.process_and_save_documents()

# Create an instance of the class and call the method
combiner = JsonToCsvCombiner(target_folders, output_csv_folder)
combiner.combine_json_to_csv()
