import pandas as pd
import numpy as np

# Function: Clean data by loading df, exploding the columns, replacing N/A with NaN values, dropping NaN columns, loading df into an Excel file
file_path = 'data.json'
def clean_data(file_path):
    try:
        df = pd.read_json(file_path)
        df = df.explode(['title', 'description', 'opened_on', 'link']).reset_index(drop=True)
        df.index = df.index + 1
        df = df.replace('N/A', np.nan)
        df.dropna(inplace=True)
        print('Dataframe has been cleaned.')

        df.to_excel('internships.xlsx')
        print('Dataframe has been loaded into an excel file.')
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    clean_data(file_path)