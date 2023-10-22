import pandas as pd
import numpy as np

class DataCleaning:
    def __init__(self, csv_file_path):
        self.df = pd.read_csv(csv_file_path)

    def general_column_mapping(self, column_mapping):
        if not column_mapping:
            return self.df

        new_column, column_dict = column_mapping.popitem()
        conditions = []
        values = []
        for column, value in column_dict.items():
            conditions.append(self.df[column] == 'selected')
            values.append(value)

        self.df[new_column] = np.select(conditions, values, default='unknown')
        return self.general_column_mapping(column_mapping)

    def med_exam_column_mapping(self, column_mapping):
        if not column_mapping:
            return self.df

        new_column, column = column_mapping.popitem()
        condition = pd.notna(self.df[column])
        value = self.df[column]

        self.df[new_column] = np.where(condition, value, 'Normal')
        return self.med_exam_column_mapping(column_mapping)

    def create_csv(self,desired_columns_order, output_file_name):
        self.df = self.df[desired_columns_order]
        self.df.to_csv(output_file_name, index=False)
        return self.df