from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.core.serialization import AzureJSONEncoder
import os
import json

class DocumentProcessor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.endpoint = os.getenv("ENDPOINT")
        self.model_id = os.getenv("MODEL_ID")
        self.input_folder = "forms"
        
        # TODO: Change output_folder to output_txt_data
        self.output_folder = "output"

    def get_target_folder(self, form_name):
        form_name = form_name.lower()
        
        if "hiv" in form_name:
            return "hiv_cert"
        elif "psychological evaluation form" in form_name:
            return "psychological_eval"
        elif "medical certificate for landbased" in form_name:
            return "med_cert_landbase"
        elif "medical examination report for landbased" in form_name:
            return "med_exam_landbase"
        elif "medical certificate for service at sea" in form_name:
            return "med_cert_seafarers"
        elif "medical examination report for seafarers" in form_name:
            return "med_exam_seafarers"
        else:
            return "other"

    def process_document(self, document_path, document_client, target_folder):
        with open(document_path, "rb") as f:
            poller = document_client.begin_analyze_document(
                model_id=self.model_id, document=f
            )

        result = poller.result()

        if result.documents:
            form_name = result.documents[0].fields.get("form_name", {}).value.lower()
            target_folder = self.get_target_folder(form_name)

            if target_folder:
                return result, target_folder, form_name
        return None, None, None

    def create_json(self, target_folder, file_name, result, form_name):
        file_output_folder = os.path.join(self.output_folder, target_folder)
        os.makedirs(file_output_folder, exist_ok=True)
        output_file = os.path.join(file_output_folder, f"{os.path.splitext(file_name)[0]}.json".lower())
        field_names_to_process = ["sense_of_responsibility", "emotional_stability", "objectivity", "motivation", "interpersonal_personal_adjustment", "goal_orientation"]  # Add your desired field names here
        data_dict = {}

        if "psychological evaluation form" in form_name.lower():
            for idx, document in enumerate(result.documents):
                for name, field in document.fields.items():
                    if name in field_names_to_process:
                        if isinstance(field.value, dict):
                            for row_key, row_value in field.value.items():
                                if 'COLUMN1' in row_value.value and any(cell.value == 'selected' for cell in row_value.value.values()):
                                    column1_value = row_value.value['COLUMN1'].value
                                    for column, cell in row_value.value.items():
                                        if cell.value == 'selected':
                                            data_dict[column1_value] = column

                    else:
                        if isinstance(field.value, dict):
                            for key, value in field.value.items():
                                data_dict[key] = value.get('value') if isinstance(value, dict) else value
                        else:
                            data_dict[name] = field.value
        
        else:
            for document in result.documents:
                for name, field in document.fields.items():
                    field_value = field.value if field.value else field.content
                    data_dict[name] = field_value

        with open(output_file, "w") as json_file:
            json.dump(data_dict, json_file, indent=4, cls=AzureJSONEncoder)
        
        print(f"Processed {file_name}. Recognized text saved to {output_file} in folder {target_folder}")

    def process_and_save_documents(self):
        document_analysis_client = DocumentAnalysisClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.api_key)
        )
        
        file_list = os.listdir(self.input_folder)
        
        for file_name in file_list:
            file_path = os.path.join(self.input_folder, file_name)
            print(f"""
                file_name: {file_name}
                file_path: {file_path}
            """)
            
            result, target_folder, form_name = self.process_document(file_path, document_analysis_client, self.output_folder)
            
            if result:
                self.create_json(target_folder, file_name, result, form_name)
        
        print("Processing complete")