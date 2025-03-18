import pandas as pd
import os
from tkinter import filedialog
import numpy as np
from datetime import datetime


def get_current_datetime():

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def import_data(file_directory):

    data_list = []

    file_paths = [os.path.join(file_directory, f) for f in os.listdir(file_directory) if f.endswith('.dat')]

    for file_path in file_paths:

        with open(file_path, 'r') as f:

            headers = f.readline().strip().split()

        data = np.loadtxt(file_path, skiprows=1)

        data_list.append(data)
    
    data_list_array = np.array(data_list)

    return data_list_array, headers


def calculate_mean_values(all_data_array, headers):

    mean_data = np.mean(all_data_array, axis=0)

    mean_dataframe = pd.DataFrame(mean_data, columns = headers)

    return mean_dataframe


def export_data(file_directory,mean_dataframe):

    timestamp = get_current_datetime()

    export_file_path = os.path.join(file_directory, f"{timestamp}_means.csv")

    mean_dataframe.to_csv(export_file_path)
    

def main():

    file_directory = filedialog.askdirectory()

    data_list_array, headers = import_data(file_directory)

    mean_dataframe = calculate_mean_values(data_list_array, headers)

    export_data(file_directory, mean_dataframe)


main()

