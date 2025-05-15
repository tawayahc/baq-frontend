import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class DataLoader:
    def __init__(self):
        self.file_path = os.path.join(CURRENT_DIR, '../../data/mockup_data.csv')
        self.data = self.load_data(-1)

    def load_data(self, last_index:int):
        try:
            self.data = pd.read_csv(self.file_path)
            if last_index > 0:
                return self.data.iloc[:last_index]
            if last_index == -1:
                return self.data
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return None
        except pd.errors.EmptyDataError:
            print("No data found in the file.")
            return None
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            return None

    def get_data(self, index: int):
        if self.data is not None and index < len(self.data):
            return self.data.iloc[[index]]
        else:
            print("Data not loaded or index out of range.")
            return pd.DataFrame()