import base64
import magic
from ctypes.util import find_library
import requests
import os
import time
import json
from dotenv import load_dotenv
import threading
from concurrent.futures import ThreadPoolExecutor
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.core.serialization import AzureJSONEncoder


class DocumentProcessor:
    def __init__(self):
        load_dotenv()
        self.mime = magic.Magic(mime=True, magic_file=find_library('magic'))
        self.supported_mime_types = [
            "application/pdf",
            "image/jpeg",
            "image/png",
        ]
        self.endpoint, self.classifier_id, self.api_version, self.api_key = self.get_api_credentials()
        self.output_folder = "output_json"
    def get_api_credentials(self):
        return (
            os.getenv("ENDPOINT"),
            os.getenv("CLASSIFIER_ID"),
            os.getenv("API_VERSION"),
            os.getenv("API_KEY"),
        )
    
    def encode_document(self, file_path):
        with open(file_path, 'rb') as document:
            encoded_docu = base64.b64encode(document.read()).decode()
        return encoded_docu

    def get_mime_type(self, encoded_docu):
        mime_type = self.mime.from_buffer(base64.b64decode(encoded_docu))
        print(f"MIME Type: {mime_type}")
        return mime_type

    def post_request_document(self, encoded_docu):
        print(f"{self.endpoint}, {self.classifier_id}, {self.api_version}, {self.api_key}")
        payload = {
            "base64Source": encoded_docu
        }
        url = f"{self.endpoint}/formrecognizer/documentClassifiers/{self.classifier_id}:analyze?api-version={self.api_version}"
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))        
        print(response)
        return response         
    
    def check_analysis_status(self, response):
        status_url = response.headers['Operation-Location']
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }

        while True:
            status_response = requests.get(status_url, headers=headers)
            status_data = status_response.json()
            status = status_data['status']
            print(status)

            if status == 'succeeded':
                return self.process_analysis_result(status_data)
            elif status == 'failed':
                print("Analysis failed. Returning None")
                return None
            else:
                time.sleep(5)

    def process_analysis_result(self, status_data):
        if 'analyzeResult' in status_data:
            result = status_data['analyzeResult']['documents'][0]
            doc_type = result['docType']
            confidence = result['confidence']
            print(f"""
                  Analysis completed. Results:
                  Document Type: {doc_type} 
                  Confidence: {confidence}
                  """)
            if confidence < 0.15:
                print("Confidence level is less than 15%. Returning None")
                return None
            else:
                print("Returning doc_type")
                return doc_type
        else:
            print("Analysis result not found in response. Returning None")
            return None
        
    def get_model_id(self, doc_type):
        model_id = {
            "hiv certificate": "hiv_cert_model",
            "psychological evaluation form": "psycho_eval_model",
            "landbase certificate": "med_landbase_cert_model",
            "landbase medical exam": "med_landbase_exam_model",
            "seafarers certificate": "med_seafarers_cert_model",
            "seafarers medical exam": "med_seabased_exam_model"
        }
        id = model_id.get(doc_type.lower())
        print(id)
        return id

    def get_target_folder(self, doc_type):
        target_folder = {
            "hiv certificate": "hiv_cert_json",
            "landbase certificate": "med_landbase_cert_json",
            "landbase medical exam": "med_landbase_exam_json",
            "psychological evaluation form": "psycho_eval_json",
            "seafarers certificate": "med_seafarers_cert_json",
            "seafarers medical exam": "med_seafarers_exam_json"
        }
        target = target_folder.get(doc_type.lower())
        print(target)
        return target
    
    def process_document(self, document_path, document_client, model_id):
        print(f"""
              Processing Document
              """)
        with open(document_path, "rb") as f:
            poller = document_client.begin_analyze_document(
                model_id=model_id, document=f
            )
        result = poller.result()

        if result.documents:
            return result
        return None
    
    def create_json(self, result, target_folder, file_name, doc_type):
        file_output_folder = os.path.join(self.output_folder, target_folder)
        os.makedirs(file_output_folder, exist_ok=True)
        output_file = os.path.join(file_output_folder, f"{os.path.splitext(file_name)[0]}.json".lower())

        field_names_to_process = [
            "sense_of_responsibility", 
            "emotional_stability", 
            "objectivity", 
            "motivation", 
            "interpersonal_personal_adjustment", 
            "goal_orientation"
            ] 
        
        data_dict = {}

        if "psychological evaluation form" == doc_type.lower():
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

        
    def process_single_document(self, file_path, file_name):
        print(f"file_path: {file_path}, file_name: {file_name}")
        encoded_docu = self.encode_document(file_path)
        mime_type = self.get_mime_type(encoded_docu)
        
        if mime_type not in self.supported_mime_types:
            print("Skipping document due to unsupported MIME type.")
            return None

        response = self.post_request_document(encoded_docu)

        if response.status_code == 202:
            doc_type = self.check_analysis_status(response)
            id = self.get_model_id(doc_type) 
            target_folder = self.get_target_folder(doc_type)
            document_analysis_client = DocumentAnalysisClient(
                endpoint=self.endpoint, credential=AzureKeyCredential(self.api_key)
            )
            result = self.process_document(file_path, document_analysis_client, id)

            self.create_json(result, target_folder, file_name, doc_type)
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response body:")
            print(response.text)
            return None