from dashlabs import DocumentProcessor
from dashlabs import JsonToCsvCombiner
from dashlabs import ColumnCleaning
import pandas as pd
import numpy as np


# Process the documents
document_processor = DocumentProcessor()
document_processor.process_and_save_documents()

# Define the target folders and output folder
target_folders = [
    "hiv_cert",
    "med_exam_landbase",
    "med_exam_seafarers",
    "med_cert_landbase",
    "med_cert_seafarers",
]
output_csv_folder = "output_uncleaned_csv"


# Create an instance of the class and call the method
combiner = JsonToCsvCombiner(target_folders, output_csv_folder)
combiner.combine_json_to_csv()



# HIV Certificate 
file_path = 'output_uncleaned_csv\hiv_cert\combined_data_hiv_cert.csv'
hiv_cert = ColumnCleaning(file_path)
column_mapping = {
    'result': {'nonreactive': 'nonreactive', 'reactive': 'reactive'},
    'screening_test_used': {'is_rapid': 'Rapid', 'is_particle': 'Particle Agglunation', 'is_eia_cmia_elfa': 'EIA/CMIA/ELFA', 'is_others': 'Others'},
}
desired_columns_order = [
    'form_name', 'name', 'address', 'age', 'gender', 'civil_status', 'date',
    'result', 'screening_test_used', 'certify_name', 'physician', 'license_no',
    'date_medical_exam', 'technologist', 'hiv_cert_no', 'expiry_ date', 'pathologist'
]
hiv_cert.general_column_mapping(column_mapping)
hiv_cert.create_csv(desired_columns_order, 'cleaned_hiv_record.csv')

# ---------------------------------------------------------------------------------- #

# Landbase Medical Certificate
file_path = 'output_uncleaned_csv\med_cert_landbase\combined_data_med_cert_landbase.csv'
landbase_certificate = ColumnCleaning(file_path)
column_mapping = {
    'gender': {'is_male': 'Male', 'is_female': 'Female'},
    'civil_status': {'is_single': 'Single', 'is_married': 'Married'},
    'hearing': {'hear_yes': 'Yes', 'hear_no': 'No'},
    'sight': {'sight_yes': 'Yes', 'sight_no': 'No'},
    'vision': {'vision_yes': 'Yes', 'vision_no': 'No'},
    'psychological': {'psych_test_yes': 'Yes', 'psych_test_no': 'No'},
    'suffer_medical_condition': {'suffer_med_con_yes': 'Yes', 'suffer_med_con_no': 'No'},
    'fit_for_job': {'is_fit': 'fit', 'is_unfit': 'No'}
}
desired_columns_order = [
    'form_name','last_name','first_name','mid_name','age','dob','place_of_birth',
    'nationality','gender','civil_status','religion','address','passport_num',
    'destination','position','employer', 'hearing','sight','vision','psychological',
    'suffer_medical_condition','fit_for_job','physician','exam_date','med_doctor',
    'date_sign','issued_date','expiration_date'
]
landbase_certificate.general_column_mapping(column_mapping)
landbase_certificate.create_csv(desired_columns_order, 'cleaned_landbase_cert_record.csv')

# ---------------------------------------------------------------------------------- #

# Seabase Medical Certificate
file_path = 'output_uncleaned_csv\med_cert_seafarers\combined_data_med_cert_seafarers.csv'
seabase_certificate = ColumnCleaning(file_path)
column_mapping = {
    'gender': {'is_male': 'Male', 'is_female': 'Female'},
    'civil_status': {'is_single': 'Single', 'is_married': 'Married'},
    'position_applied': {'is_deck': 'Deck', 'is_engine': 'Engine', 'is_catering': 'Catering', 'is_other': 'others'},
    'documents_checked': {'documents_checked_yes': 'Yes', 'documents_checked_no': 'No'},
    'hearing_stwcode': {'hearing_stwcode_yes': 'Yes', 'hearing_stwcode_no': 'No'},
    'unaided_hearing': {'unaided_hearing_yes': 'Yes', 'unaided_hearing_no': 'No'},
    'visual_acuity': {'visual_acuity_yes': 'Yes', 'visual_acuity_no': 'No'},
    'colour_vision': {'colour_vision_yes': 'Yes', 'colour_vision_no': 'No'},
    'visual_aids': {'is_spectacles': 'Spectacles', 'is_contact_lenses': 'Contact Lenses'},
    'lookout_duties': {'lookout_duties_yes': 'Yes', 'lookout_duties_no': 'No'},
    'restrictions': {'restrictions_yes': 'Yes', 'restrictions_no': 'No'},
    'suffering_med_conditions': {'suffering_yes': 'Yes', 'suffering_no': 'No'},
    'fit_for_duty': {'fit_for_duty_yes': 'Fit', 'unfit_for_duty_no': 'Unfit'},
}
desired_columns_order = [
    'form_name','surname','first_name','middle_name','dob','gender','age',
    'place_of_birth','nationality','civil_status','religion',
    'address','passport_no','seaman_book_no','position_applied','company','documents_checked','hearing_stwcode',
    'unaided_hearing','visual_acuity','colour_vision','visual_aids',
    'date_of_last_colourvisiontest','lookout_duties','restrictions',
    'limiting_restrictions','suffering_med_conditions','exam_given_to',
    'fit_for_duty','physician','date_of_exam','approved_by','issuing_auth','address_auth',
    'certifying_auth','license_num','seaferer_signature','signature_date',
    'date_of_issuance','date_of_expiry',
]
seabase_certificate.general_column_mapping(column_mapping)
seabase_certificate.create_csv(desired_columns_order, 'cleaned_seabase_cert_record.csv')

# ---------------------------------------------------------------------------------- #

# Landbase Medical Exam
file_path = 'output_uncleaned_csv\med_exam_landbase\combined_data_med_exam_landbase.csv'
landbase_exam = ColumnCleaning(file_path)
gender_and_status = {
    'gender': {'is_male': 'Male', 'is_female': 'Female'},
    'civil_status': {'is_single': 'Single', 'is_married': 'Married'},
}
medical_history = {
    'head_or_neck_injury': {'is_head_injury_yes': "Yes", 'is_head_injury_no': 'No'},
    'frequent_headaches': {'is_frequent_headache_yes': 'Yes', 'is_frequent_headache_no': 'No'},
    'frequent_diziness': {'is_frequent_diziness_yes': 'Yes', 'is_frequent_diziness_no': 'No'},
    'neurological_disorder': {'is_neurological_disorder_yes': 'Yes', 'is_neurological_disorder_no': 'No'},
    'sleep_disorder': {'is_sleep_disorder_yes': 'Yes', 'is_sleep_disorder_no': 'No'},
    'mental_disorder': {'is_mental_disorder_yes': 'Yes', 'is_mental_disorder_no': 'No'},
    'eye_problem': {'is_eye_problem_yes': 'Yes', 'is_eye_problem_no': 'No'},
    'ear_disorder': {'is_ear_disorder_yes': 'Yes', 'is_ear_disorder_no': 'No'},
    'nose_throat_disorder': {'is_nose_throat_disorder_yes': 'Yes', 'is_nose_throat_disorder_no': 'No'},
    'tuberculosis': {'is_tuberculosis_yes': 'Yes', 'is_tuberculosis_no': 'No'},
    'lung_disorder': {'is_lung_disorder_yes': 'Yes', 'is_lung_disorder_no': 'No'},
    'high_blood_pressure': {'is_high_blood_pressure_yes': 'Yes', 'is_high_blood_pressure_no': 'No'},
    'heart_problem': {'is_heart_disease_yes': 'Yes', 'is_heart_disease_no': 'No'},
    'rheumatic_fever': {'is_rheumatic_yes': 'Yes', 'is_rheumatic_no': 'No'},
    'diabetes': {'is_diabetes_yes': 'Yes', 'is_diabetes_no': 'No'},
    'endocrine_disorder': {'is_endocrine_disorders_yes': 'Yes', 'is_endocrine_disorder_no': 'No'},
    'cancer_tumor': {'is_cancer_yes': 'Yes', 'is_cancer_no': 'No'},
    'blood_disorder': {'is_blood_disorder_yes': 'Yes', 'is_blood_disorder_no': 'No'},
    'stomach_disorder': {'is_stomach_pain_yes': 'Yes', 'is_stomach_pain_no': 'No'},
    'abdominal_disorder': {'is_abdominal_disorder_yes': 'Yes', 'is_abdominal_disorder_no': 'No'},
    'gynaecological_disorder': {'is_gyna_disorder_yes': 'Yes', 'is_gyna_disorder_no': 'No'},
    'kidney_bladder_disorder': {'is_bladder_disorder_yes': 'Yes', 'is_bladder_disorder_no': 'No'},
    'back_injury': {'is_back_injury_yes': 'Yes', 'is_back_injury_no': 'No'},
    'familial_disorder': {'is_familial_disorder_yes': 'Yes', 'is_familial_disorder_no': 'No'},
    'sexually_transmittable_disease': {'is_sexuall_transmit_disease_yes': 'Yes', 'is_sexual_transmit_disease_no': 'No'},
    'tropical_disease': {'is_typical_diseases_yes': 'Yes', 'is_typical_diseases_no': 'No'},
    'schistosomiasis': {'is_schistosomiasis_yes': 'Yes', 'is_schistosomiasis_no': 'No'},
    'asthma': {'is_asthma_yes': 'Yes', 'is_asthma_no': 'No'},
    'allergies': {'is_allergies_yes': landbase_exam.df['allergies'], 'is_allergies_no': "No"},
    'operation_history': {'is_operation_yes': landbase_exam.df['operation'], 'is_operation_no': "No"},
    'signed_of_as_sick': {'is_signed_of_as_sick_yes': 'Yes', 'is_signed_of_as_sick_no': 'No'},
    'hospitalized': {'is_hospitalized_yes': 'Yes', 'is_hospitalized_no': 'No'},
    'declared_unfit_before': {'is_declared_unfit_before_yes': 'Yes', 'is_declared_unfit_before_no': 'No'},
    'medical_certificate_revoked': {'is_med_cert_restrict_yes': 'Yes', 'is_med_cert_restrict_no': 'No'},
    'aware_medical_problem': {'is_med_prob_yes': 'Yes', 'is_med_prob_no': 'No'},
    'feel_fit': {'feel_fit_yes': 'Yes', 'feel_fit_no': 'No'},
 'allergic_medication': {'is_allergic_medication_yes': landbase_exam.df['medication_allergy'], 'is_allergic_medication_no': "No" },
    'taking_medication': {'is_taking_medication_yes':  landbase_exam.df['medications'], 'is_taking_medication_no': "No"},
}
medical_exam = {
    'color_vision': {'color_vision_adequate': 'Adequate', 'color_vision_defective': 'Defective'},
    'hearing_right': {'hear_ear_right_adquate': 'Adequate', 'hear_ear_right_inadequate': 'Inadequate'},
    'hearing_left': {'hear_ear_left_adequate': 'Adequate', 'hear_ear_left_inadequate': 'Inadequate'},
    'clarity_speech': {'clarity_speech_adquate': 'Adequate', 'clarity_speech_inadequate': 'Inadequate'},
}
medical_result = {
    'x-ray': {'is_xray_normal': 'Normal', 'is_xray_with_findings': 'With Findings'},
    'ecg': {'is_ecg_normal': 'Normal', 'is_ecg_with_findings': 'With Findings'},
    'cbc': {'is_cbc_normal': 'Normal', 'is_cbc_with_findings': 'With Findings'},
    'urinalysis': {'is_urinalysis_normal': 'Normal', 'is_urinalysis_with_findings': 'With Findings'},
    'stool': {'is_stool_normal': 'Normal', 'is_stool_with_findings': 'With Findings'},
    'hepatitis_b': {'is_hepa_reactive': 'Reactive', 'is_hepa_non-reactive': 'Non-Reactive'},
    'hiv_test': {'is_hiv_test_reactive': 'Reactive', 'is_hiv_test_non-reactive': 'Non-Reactive'},
    'rpr': {'is_rpr_reactive': 'Reactive', 'is_rpr_non-reactive': 'Non-Reactive'},
    'psychological_test': {'is_psycho_normal': 'Normal', 'is_psycho_for_eval': 'For Further Evaluation'},
}
medical_summary = {
    'basic_doh_med_exam': {'basic_doh_med_exam_pass': 'PASSED', 'is_basic_doh_exam_fail': 'WITH SIGNIFICANT FINDINGS'},
    'additional_lab_pass': {'is_additional_lab_pass': 'PASSED', 'is_additional_lab_fail': 'WITH SIGNIFICANT FINDINGS'},
    'host_medical_lab': {'is_host_med_lab_pass': 'PASSED', 'is_host_med_lab_fail': 'WITH SIGNIFICANT FINDINGS'},
    'is_medically_fit': {'is_fit': 'FIT', 'is_unfit': 'UNFIT'},
}
general_column_mapping = {**gender_and_status, **medical_history, **medical_exam, **medical_result, **medical_summary}
med_exam_column_mapping = {
    'skin': 'skin_findings',
    'head_neck_scalp': 'head_neck_scalp_findings',
    'eyes_external' : 'eyes_external_findings',
    'pupils_ophthaimoscopic' : 'pupils_findings',
    'ears' : 'ears_findings',
    'nose_sinuses' : 'nose_sinus_findings',
    'mouth_throat' : 'mouth_throat_findings',
    'mouth_throat' : 'mouth_throat_findings',
    'neck_lymph_nodes_thyroid': 'neck_findings',
    'chest_breast_axilla': 'chest_findings',
    'lungs': 'lungs_findings',
    'heart': 'heart_findings',
    'abdomen': 'abdomen_findings',
    'back': 'back_findings',
    'anus_rectum': 'anus_rectum_findings',
    'genito_urinary_system': 'genito_findings',
    'inguinals_genitals': 'genitals_findings',
    'extremities': 'extremities_findings',
    'reflexes': 'speed_findings',
    'dental': 'dental_findings',
}
personal_data_order = [
    "form_name","last_name","first_name","mid_name","age","dob","place_of_birth",
    "nationality","gender", "civil_status","religion","address","passport_num",
    "destination","position", "employer"
]
medical_history_order = [
    "head_or_neck_injury", "frequent_headaches",
    "frequent_diziness", "neurological_disorder", "sleep_disorder", "mental_disorder",
    "eye_problem", "ear_disorder", "nose_throat_disorder", "tuberculosis", "lung_disorder",
    "high_blood_pressure", "heart_problem", "rheumatic_fever", "diabetes",
    "endocrine_disorder", "cancer_tumor", "blood_disorder", "stomach_disorder",
    "abdominal_disorder", "gynaecological_disorder", "date_last_menstruation",
    "kidney_bladder_disorder", "back_injury", "familial_disorder", "sexually_transmittable_disease",
    "tropical_disease", "schistosomiasis", "asthma", "allergies", "operation_history",
    "signed_of_as_sick", "hospitalized", "declared_unfit_before", "medical_certificate_revoked",
    "aware_medical_problem", "feel_fit", "allergic_medication", "medication_allergy",
    "taking_medication", "medications"
]
medical_exam_order = [
    "height","weight","blood_pressure","pulse_rate",
    "rhythm","respiration","bmi","far_vision_uncorrected","far_vision_corrected",
    "near_vision_uncorrected","near_vision_corrected","color_vision", "hearing_right",
    "hearing_left", "clarity_speech","skin", "head_neck_scalp", "eyes_external",
    'pupils_ophthaimoscopic', "ears", "nose_sinuses", "mouth_throat",
    "neck_lymph_nodes_thyroid", "chest_breast_axilla", "lungs", "heart", "abdomen",
    "back", "anus_rectum", "genito_urinary_system", "inguinals_genitals", "extremities",
    "reflexes", "dental",
]
result_order = [
    "x-ray","x-ray_findings","ecg", "ecg_findings","cbc", "cbc_findings",
    "urinalysis", "urinalysis_findings", "stool", "stool_findings","hepatitis_b", "hiv_test", "rpr",
    "blood_type","psychological_test","addtional_test",
]
summary_order = [
     "basic_doh_med_exam", "additional_lab_pass", "host_medical_lab","is_medically_fit"
]
end_form_order = [
    "date_med_exm","date_med_expire","med_exam_report_no","physician","license_no","clinic_address",
    "clinic_name","date_sign",
]

desired_columns_order = [*personal_data_order, *medical_history_order, *medical_exam_order, *result_order, *summary_order, *end_form_order]

general_table_cleaning = landbase_exam.general_column_mapping(general_column_mapping)
med_exam_cleaning = landbase_exam.med_exam_column_mapping(med_exam_column_mapping)
landbase_exam.create_csv(desired_columns_order, 'cleaned_landbase_exam_record.csv')

# ---------------------------------------------------------------------------------- #

#Seabase Medical Exam
file_path = 'output_uncleaned_csv\med_exam_seafarers\combined_data_med_exam_seafarers.csv'
seabase_exam = ColumnCleaning(file_path)
gender_and_status = {
    'gender': {'is_male': 'Male', 'is_female': 'Female'},
    'civil_status': {'is_single': 'Single', 'is_married': 'Married'},
    'position_applied': {'is_deck': 'Deck', 'is_engine': 'Engine', 'is_catering': 'Catering', 'others': seabase_exam.df['position_applied_specify']},

}
medical_history = {
    'head_or_neck_injury': {'is_head_injury_yes': "Yes", 'is_head_injury_no': 'No'},
    'frequent_headaches': {'is_frequent_headache_yes': 'Yes', 'is_frequent_headache_no': 'No'},
    'frequent_diziness': {'is_frequent_diziness_yes': 'Yes', 'is_frequent_diziness_no': 'No'},
    'neurological_disorder': {'is_neurological_disorder_yes': 'Yes', 'is_neurological_disorder_no': 'No'},
    'sleep_disorder': {'is_sleep_disorder_yes': 'Yes', 'is_sleep_disorder_no': 'No'},
    'mental_disorder': {'is_mental_disorder_yes': 'Yes', 'is_mental_disorder_no': 'No'},
    'eye_problem': {'is_eye_problem_yes': 'Yes', 'is_eye_problem_no': 'No'},
    'ear_disorder': {'is_ear_disorder_yes': 'Yes', 'is_ear_disorder_no': 'No'},
    'nose_throat_disorder': {'is_nose_throat_disorder_yes': 'Yes', 'is_nose_throat_disorder_no': 'No'},
    'tuberculosis': {'is_tuberculosis_yes': 'Yes', 'is_tuberculosis_no': 'No'},
    'lung_disorder': {'is_lung_disorder_yes': 'Yes', 'is_lung_disorder_no': 'No'},
    'high_blood_pressure': {'is_high_blood_pressure_yes': 'Yes', 'is_high_blood_pressure_no': 'No'},
    'heart_problem': {'is_heart_disease_yes': 'Yes', 'is_heart_disease_no': 'No'},
    'rheumatic_fever': {'is_rheumatic_yes': 'Yes', 'is_rheumatic_no': 'No'},
    'diabetes': {'is_diabetes_yes': 'Yes', 'is_diabetes_no': 'No'},
    'endocrine_disorder': {'is_endocrine_disorders_yes': 'Yes', 'is_endocrine_disorder_no': 'No'},
    'cancer_tumor': {'is_cancer_yes': 'Yes', 'is_cancer_no': 'No'},
    'blood_disorder': {'is_blood_disorder_yes': 'Yes', 'is_blood_disorder_no': 'No'},
    'stomach_disorder': {'is_stomach_pain_yes': 'Yes', 'is_stomach_pain_no': 'No'},
    'abdominal_disorder': {'is_abdominal_disorder_yes': 'Yes', 'is_abdominal_disorder_no': 'No'},
    'gynaecological_disorder': {'is_gyna_disorder_yes': 'Yes', 'is_gyna_disorder_no': 'No'},
    'kidney_bladder_disorder': {'is_bladder_disorder_yes': 'Yes', 'is_bladder_disorder_no': 'No'},
    'back_injury': {'is_back_injury_yes': 'Yes', 'is_back_injury_no': 'No'},
    'familial_disorder': {'is_familial_disorder_yes': 'Yes', 'is_familial_disorder_no': 'No'},
    'sexually_transmittable_disease': {'is_sexuall_transmit_disease_yes': 'Yes', 'is_sexual_transmit_disease_no': 'No'},
    'tropical_disease': {'is_typical_diseases_yes': 'Yes', 'is_typical_diseases_no': 'No'},
    'schistosomiasis': {'is_schistosomiasis_yes': seabase_exam.df['yes_schist_date'], 'is_schistosomiasis_no': 'No'},
    'asthma': {'is_asthma_yes': 'Yes', 'is_asthma_no': 'No'},
    'allergies': {'is_allergies_yes':  seabase_exam.df['allergies_specify'], 'is_allergies_no': "No"},
    'signed_of_as_sick': {'is_signed_of_as_sick_yes': 'Yes', 'is_signed_of_as_sick_no': 'No'},
    'hospitalized': {'is_hospitalized_yes': 'Yes', 'is_hospitalized_no': 'No'},
    'declared_unfit_before': {'is_declared_unfit_before_yes': 'Yes', 'is_declared_unfit_before_no': 'No'},
    'medical_certificate_revoked': {'is_med_cert_restrict_yes': 'Yes', 'is_med_cert_restrict_no': 'No'},
    'aware_medical_problem': {'is_med_prob_yes': 'Yes', 'is_med_prob_no': 'No'},
    'feel_fit': {'feel_fit_yes': 'Yes', 'feel_fit_no': 'No'},
    'allergic_medication': {'is_allergic_medication_yes': seabase_exam.df['medication_allergy'], 'is_allergic_medication_no': "No" },
    'taking_medication': {'is_taking_medication_yes':  seabase_exam.df['medications'], 'is_taking_medication_no': "No"},
}
medical_exam = {
    'color_vision': {'color_vision_adequate': 'Adequate', 'color_vision_defective': 'Defective'},
    'hearing_right': {'hear_ear_right_adquate': 'Adequate', 'hear_ear_right_inadequate': 'Inadequate'},
    'hearing_left': {'hear_ear_left_adequate': 'Adequate', 'hear_ear_left_inadequate': 'Inadequate'},
    'clarity_speech': {'clarity_speech_adquate': 'Adequate', 'clarity_speech_inadequate': 'Inadequate'},
}
medical_result = {
    'x-ray': {'is_xray_normal': 'Normal', 'is_xray_with_findings': 'With Findings'},
    'ecg': {'is_ecg_normal': 'Normal', 'is_ecg_with_findings': 'With Findings'},
    'cbc': {'is_cbc_normal': 'Normal', 'is_cbc_with_findings': 'With Findings'},
    'urinalysis': {'is_urinalysis_normal': 'Normal', 'is_urinalysis_with_findings': 'With Findings'},
    'stool': {'is_stool_normal': 'Normal', 'is_stool_with_findings': 'With Findings'},
    'hepatitis_b': {'is_hepa_reactive': 'Reactive', 'is_hepa_non-reactive': 'Non-Reactive'},
    'hiv_test': {'is_hiv_test_reactive': 'Reactive', 'is_hiv_test_non-reactive': 'Non-Reactive'},
    'rpr': {'is_rpr_reactive': 'Reactive', 'is_rpr_non-reactive': 'Non-Reactive'},
    'psychological_test': {'is_psycho_normal': 'Normal', 'is_psycho_for_eval': 'For Further Evaluation'},
}
medical_summary = {
    'basic_doh_med_exam': {'basic_doh_med_exam_pass': 'PASSED', 'is_basic_doh_exam_fail': 'WITH SIGNIFICANT FINDINGS'},
    'additional_lab_pass': {'is_additional_lab_pass': 'PASSED', 'is_additional_lab_fail': 'WITH SIGNIFICANT FINDINGS'},
    'host_medical_lab': {'is_host_med_lab_pass': 'PASSED', 'is_host_med_lab_fail': 'WITH SIGNIFICANT FINDINGS'},
    'look_out_duty': {'is_fit': 'FIT', 'is_unfit': 'UNFIT'},
    'deck_service': {'fit_deck_service': 'FIT', 'unfit_deck_service': 'UNFIT'},
    'engine_service': {'fit_engine_service': 'FIT', 'unfit_engine_service': 'UNFIT'},
    'catering_service': {'fit_catering_service': 'FIT', 'unfit_catering_service': 'UNFIT'},
    'other_service': {'fit_other_services': 'FIT', 'unfit_other_services': 'UNFIT'},
    'restrictions': {'with_restrictions': seabase_exam.df['describe_restrictions'], 'without_restrictions': 'WITHOUT RESTRICTIONS'},
    'visual_aids': {'visual_aids_yes': 'Yes', 'visual_aids_no': 'No'},
}
general_column_mapping = {**gender_and_status, **medical_history, **medical_exam, **medical_result, **medical_summary}
med_exam_column_mapping = {
    'skin': 'skin_findings',
    'head_neck_scalp': 'head_neck_findings',
    'eyes_external' : 'eyes_external_findings',
    'pupils_ophthaimoscopic' : 'pupils_findings',
    'ears' : 'ears_findings',
    'nose_sinuses' : 'nose_sinus_findings',
    'mouth_throat' : 'mouth_throat_findings',
    'mouth_throat' : 'mouth_throat_findings',
    'neck_lymph_nodes_thyroid': 'neck_findings',
    'chest_breast_axilla': 'chest_findings',
    'lungs': 'lungs_findings',
    'heart': 'heart_findings',
    'abdomen': 'abdomen_findings',
    'back': 'back_findings',
    'anus_rectum': 'anus_rectum_findings',
    'genito_urinary_system': 'urinary_system_findings',
    'inguinals_genitals': 'genitals_findings',
    'extremities': 'extremities_findings',
    'reflexes': 'reflexes_findings',
    'dental': 'dental_findings',
}
personal_data_order = [
    "form_name","last_name","first_name","mid_name","age","dob","place_of_birth",
    "nationality","gender", "civil_status","religion","address","passport_num","seaman_num",
    "position_applied", "employer"
]
medical_history_order = [
    "head_or_neck_injury", "frequent_headaches",
    "frequent_diziness", "neurological_disorder", "sleep_disorder", "mental_disorder",
    "eye_problem", "ear_disorder", "nose_throat_disorder", "tuberculosis", "lung_disorder",
    "high_blood_pressure", "heart_problem", "rheumatic_fever", "diabetes",
    "endocrine_disorder", "cancer_tumor", "blood_disorder", "stomach_disorder",
    "abdominal_disorder", "gynaecological_disorder", "date_last_menstruation",
    "kidney_bladder_disorder", "back_injury", "familial_disorder", "sexually_transmittable_disease",
    "tropical_disease", "schistosomiasis", "asthma", "allergies",
    "signed_of_as_sick", "hospitalized", "declared_unfit_before", "medical_certificate_revoked",
    "aware_medical_problem", "feel_fit", "allergic_medication", "medication_allergy",
    "taking_medication", "medications"
]
medical_exam_order = [
    "height","weight","blood_pressure","pulse_rate",
    "rhythm","respiration","bmi","far_vision_uncorrected","far_vision_corrected",
    "near_vision_uncorrected","near_vision_corrected","color_vision", "hearing_right",
    "hearing_left", "clarity_speech","skin", "head_neck_scalp", "eyes_external",
    'pupils_ophthaimoscopic', "ears", "nose_sinuses", "mouth_throat",
    "neck_lymph_nodes_thyroid", "chest_breast_axilla", "lungs", "heart", "abdomen",
    "back", "anus_rectum", "genito_urinary_system", "inguinals_genitals", "extremities",
    "reflexes", "dental",
]
result_order = [
    "x-ray","ecg","cbc", "urinalysis", "stool","hepatitis_b",
    "hiv_test", "rpr", "blood_type","psychological_test","addtional_test",
]
summary_order = [
     "basic_doh_med_exam", "additional_lab_pass", "host_medical_lab","look_out_duty",
     "deck_service","engine_service", "catering_service", "other_service","restrictions",
     "visual_aids"
]
end_form_order = [
    "date_med_exm","date_med_expire","med_exam_report_no","physician","license_no",
    "clinic_address","date_sign",
]
desired_columns_order = [*personal_data_order, *medical_history_order, *medical_exam_order, *result_order, *summary_order, *end_form_order]

general_table_cleaning = seabase_exam.general_column_mapping(general_column_mapping)
med_exam_cleaning = seabase_exam.med_exam_column_mapping(med_exam_column_mapping)
seabase_exam.create_csv(desired_columns_order, 'cleaned_seabase_exam_record.csv')

# ---------------------------------------------------------------------------------- #
