from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os
import json

load_dotenv()

key = os.getenv("API_KEY")
endpoint = os.getenv("ENDPOINT")
model_id = os.getenv("MODEL_ID")
input_folder = "forms"  
output_folder = "output"  

# Initialize the Document Analysis Client
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# List all files in the input folder
file_list = os.listdir(input_folder)
print(file_list)

# Iterate through the list and process images
for file_name in file_list:
    file_path = os.path.join(input_folder, file_name)
    
    
    print(f"""
          file_name : {file_name}
          file_path : {file_path}
          """)

    with open(file_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            model_id=model_id, document=f
        )

    result = poller.result()

    # Get the model used 
    doc_type = result.documents[0].doc_type.split(":")[-1]
    # Get the form name
    form_name = result.documents[0].fields.get("form_name", {}).value.lower()
    
    if form_name:
        # Determine the target folder based on the form_name
        target_folder = None
        
        if "hiv" in form_name:
            target_folder = "hiv_cert"
        
        elif "psychological evaluation form" in form_name:
            target_folder = "psychological_eval"
        
        elif "medical certificate for landbased" in form_name:
            target_folder = "med_cert_landbase"
        
        elif "medical examination report for landbased" in form_name:
            target_folder = "med_exam_landbase"    
            
        elif "medical certificate for service at sea" in form_name:
            target_folder = "med_cert_seafarers"
            
        elif "medical examination report for seafarers" in form_name:
            target_folder = "med_exam_seafarers"         
        
        else:
            target_folder = "other"

        if target_folder:
            # Create a folder for each processed file
            file_output_folder = os.path.join(output_folder, target_folder, os.path.splitext(file_name)[0])
            os.makedirs(file_output_folder, exist_ok=True)

            # Save the recognized text to a text file
            output_file = os.path.join(file_output_folder, "recognized_text.txt")
            with open(output_file, "w") as output:
                data_dict = {}
                for idx, document in enumerate(result.documents):
                    for name, field in document.fields.items():
                        
                        if field.value_type == "date":
                            data_dict[name] = field.content
                            output.write(f"{name}: {field.content}\n")
                        elif field.value:
                            data_dict[name] = field.value
                            output.write(f"{name}: {field.value}\n")
                        else:
                            data_dict[name] = field.content
                            output.write(f"{name}: {field.content}\n")

                # Save the extracted data as a dictionary in a JSON-formatted text file
                with open(os.path.join(file_output_folder, "data.json"), "w", encoding="utf-8") as data_file:
                    json.dump(data_dict, data_file, indent=4)

            # Print status indicators
            print(f"Processed {file_name}. Recognized text saved to {output_file} in folder {target_folder}")

print("Processing complete.")