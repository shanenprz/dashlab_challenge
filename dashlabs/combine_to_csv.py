import os
import pandas as pd
import json

class JsonToCsvCombiner:
    def __init__(self, target_folders, output_csv_folder):
        self.target_folders = target_folders
        self.output_csv_folder = output_csv_folder

    def combine_json_to_csv(self):
        for target_folder in self.target_folders:
            dataframes = []  # Initialize a list to store DataFrames

            # Use a list comprehension to read and process JSON files in the current target folder
            folder_path = os.path.join("output_json", target_folder)
            json_files = [file for file in os.listdir(folder_path) if file.endswith(".json")]
            for json_file in json_files:
                file_path = os.path.join(folder_path, json_file)
                with open(file_path, "r") as json_data:
                    data = json.load(json_data)
                    df = pd.DataFrame([data])  # Create a DataFrame from JSON
                    dataframes.append(df)

            # Combine all DataFrames in the list
            combined_df = pd.concat(dataframes, ignore_index=True)

            # Create a separate output folder for each category
            category_output_folder = os.path.join(self.output_csv_folder, target_folder)
            if not os.path.exists(category_output_folder):
                os.makedirs(category_output_folder)

            # Output the combined data to a CSV file in the respective category folder
            combined_csv_path = os.path.join(category_output_folder, f"combined_data_{target_folder}.csv")
            combined_df.to_csv(combined_csv_path, index=False)

            print(f"Combined data for {target_folder} saved to {combined_csv_path}")