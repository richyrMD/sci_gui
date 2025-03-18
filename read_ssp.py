import os
import pandas as pd
from tkinter import filedialog
from datetime import datetime


def get_current_datetime():

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def import_data():

    file_path = filedialog.askopenfilename()

    return file_path


def mk_export_dir(file_path,exp_dir):
    
    timestamp = get_current_datetime()

    filename = os.path.basename(file_path)

    filename_dir = os.path.splitext(filename)[0]

    export_base_dir = os.path.join(exp_dir, f"{filename_dir}_{timestamp}")

    os.makedirs(export_base_dir, exist_ok=True)
    
    metadata_file_path = os.path.join(export_base_dir, f"{filename_dir}_metadata.txt")

    data_file_path = os.path.join(export_base_dir, f"{filename_dir}_results.csv")

    return metadata_file_path, data_file_path


def split_data(file_path):
    
    metadata_lines = list()

    results_lines = list()

    is_results_section = False

    with open(file_path, "r") as file:

        for line in file:

            if "*                               Results                                 *" in line:

                is_results_section = True

            if is_results_section:

                results_lines.append(line.strip()) 

            else:

                metadata_lines.append(line.strip())

    header = None

    data = []

    results_lines = results_lines[3:]

    results_lines = [line.split("\t") for line in results_lines]

    header =results_lines[0]

    units = results_lines[1]

    for i in range(2,len(results_lines),1):
        data.append(results_lines[i])
        
    combined_header = [f"{h} [{u}]" for h, u in zip(header, units)]
    
    data = pd.DataFrame(data, columns=combined_header)
    
    return metadata_lines,data

def export_to_path(metadata, data,metadata_file_path, data_file_path):

    with open(metadata_file_path, "w", encoding="utf-8") as meta_file:
        
        meta_file.write("\n".join(metadata))
    
    data.to_csv(data_file_path, index=False)

def main():

    export_path = "/home/richard/Schreibtisch/test"

    file_path = import_data()

    metadata_file_path, data_file_path = mk_export_dir(file_path,export_path)

    metadata, data = split_data(file_path)

    export_to_path(metadata, data, metadata_file_path, data_file_path)

main()
    