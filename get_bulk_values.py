import pandas as pd 
from tkinter import filedialog
import numpy as np

#pd.set_option('display.max_rows', None)

def import_data():

    csv_file = filedialog.askopenfilename()

    #csv_file = "/home/richy/Schreibtisch/post-processing/sci_gui/testing/profile_means_inflectionpoint/test_02/20250319_092705_means.csv"

    data = pd.read_csv(csv_file)
    
    return data,csv_file


def get_approx_bulk_phase_positions(data, rho_f, rho_v):

    data["phase"] = "vap"

    magnitude_rho_f = np.log10(rho_f)

    magnitude_rho_v = np.log10(rho_v)

    magnitude_rho_f = np.round(magnitude_rho_f)

    magnitude_rho_v = np.round(magnitude_rho_v)

    data["rho[0]_magnitudes"] = np.round(np.log10(data["rho[0]"]))

    data.loc[data["rho[0]_magnitudes"] == magnitude_rho_f,"phase"] = "liq"

    data.loc[data["rho[0]_magnitudes"] == magnitude_rho_v,"phase"] = "vap"

    return data


def get_bulk_values(data):

    liq_data = data[data["phase"] == "liq"][0:10]

    vap_data = data[data["phase"] == "vap"][20:30]

    vap_mean_data = vap_data.select_dtypes(include="number").mean()

    liq_mean_data = liq_data.select_dtypes(include="number").mean()

    return vap_mean_data, liq_mean_data


def export_data(bulk_vap,bulk_liq,csv_file):

    path = csv_file.replace(".csv","")

    vap_path = csv_file + "_bulk_vap.csv"

    liq_path = csv_file + "bulk_liq.csv"
    
    bulk_vap.to_csv(vap_path)

    bulk_liq.to_csv(liq_path)


def get_bulk_values_main(data):

    rho_f = 0.73

    rho_v = 0.019

    #data, csv_file = import_data()

    data = get_approx_bulk_phase_positions(data,rho_f,rho_v)

    bulk_vap, bulk_liq = get_bulk_values(data)

    #export_data(bulk_vap,bulk_liq,csv_file)
    return bulk_vap,bulk_liq



