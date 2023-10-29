import os
import pandas as pd
import json
import numpy as np

class ColumnCleaning:
    def __init__(self, target_folder, output_csv_folder):
        self.target_folder = target_folder  # Modify to store the folder, not a list of folders
        self.output_csv_folder = output_csv_folder
    
    def apply_general_column_cleaning(self, df, column_mapping):
        if not column_mapping:
            return df

        new_column, column_dict = column_mapping.popitem()
        conditions = []
        values = []
        for column, value in column_dict.items():
            conditions.append(df[column] == 'selected')
            values.append(value)

        df[new_column] = np.select(conditions, values, default='unknown')
        return self.apply_general_column_cleaning(df, column_mapping)

    def apply_med_exam_column_cleaning(self, df, med_exam_column_cleaning):
        if not med_exam_column_cleaning:
            return df

        new_column, column = med_exam_column_cleaning.popitem()
        condition = pd.notna(df[column])
        value = df[column]

        df[new_column] = np.where(condition, value, 'Normal')
        return self.apply_med_exam_column_cleaning(df, med_exam_column_cleaning)    
        
    
    def create_new_column_dictionary(self, df, columns):
        general_column_cleaning = {}
        med_exam_column_cleaning = {}
        joiner = " "
        
        for column_name in columns:
            if '_' in column_name:
                if column_name.endswith('findings'):
                    split_column_name = column_name.split('_')
                    category = joiner.join(split_column_name[:-1])  
                    if category not in med_exam_column_cleaning:  
                        med_exam_column_cleaning[category] = {}
                    med_exam_column_cleaning[category] = column_name   
                else:
                        split_column_name = column_name.split('_')
                        category, option = joiner.join(split_column_name[:-1]), split_column_name[-1]
                        if category not in general_column_cleaning:
                            general_column_cleaning[category] = {}
                        general_column_cleaning[category][column_name] = option
            elif '-' in column_name:  
                split_column_name = column_name.split('-') 
                category, option = joiner.join(split_column_name[:-1]), split_column_name[-1]
                if category not in general_column_cleaning:
                    general_column_cleaning[category] = {}
                general_column_cleaning[category][column_name] = df[option]
        
        return general_column_cleaning, med_exam_column_cleaning
        
    def combine_json_to_csv(self, column_order):
        dataframes = []  # Initialize a list to store DataFrames

        # Use a list comprehension to read and process JSON files in the current target folder
        folder_path = os.path.join("output_json", self.target_folder)
        json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]
        for json_file in json_files:
            file_path = os.path.join(folder_path, json_file)
            with open(file_path, "r") as json_data:
                data = json.load(json_data)
                df = pd.DataFrame([data])  # Create a DataFrame from JSON
                dataframes.append(df)

        # Combine all DataFrames in the list
        combined_df = pd.concat(dataframes, ignore_index=True)
        columns = df.columns.tolist()
        general_column_dict, med_exam_column_dict = self.create_new_column_dictionary(combined_df, columns) 
        combined_df = self.apply_general_column_cleaning(combined_df, general_column_dict)
        combined_df = self.apply_med_exam_column_cleaning(combined_df, med_exam_column_dict)
        combined_df = combined_df[column_order] 
        
        # Create a separate output folder for each category
        category_output_folder = os.path.join(self.output_csv_folder, self.target_folder)
        if not os.path.exists(category_output_folder):
            os.makedirs(category_output_folder)

        # Output the combined data to a CSV file in the respective category folder
        combined_csv_path = os.path.join(category_output_folder, f"combined_data_{self.target_folder}.csv")
        combined_df.to_csv(combined_csv_path, index=False)

        print(f"Combined data for {self.target_folder} saved to {combined_csv_path}")