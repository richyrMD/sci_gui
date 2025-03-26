import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
from tkinter import filedialog
from get_bulk_values import get_bulk_values_main

import matplotlib.pyplot as plt
def import_data():

    csv_file = filedialog.askopenfilename()

    data = pd.read_csv(csv_file)
    
    return data,csv_file


def get_bulk_if_positions(data):

    bulk_vap, bulk_liq = get_bulk_values_main(data)

    x_if_vap = float()

    x_if_liq = float()
    
    if_idx = data[data["pos"] == 0.0].index[0]

    for value in data.loc[if_idx:, "rho[0]"]:

        if (abs(value - bulk_vap["rho[0]"])/bulk_vap["rho[0]"]) < 0.01:

            x_if_vap = data.loc[data["rho[0]"] == value, "pos"]

            break
    
    for value in data.loc[if_idx::-1, "rho[0]"]:

        if (abs(value - bulk_liq["rho[0]"]) / bulk_liq["rho[0]"]) < 0.01:

            x_if_liq = data.loc[data["rho[0]"] == value, "pos"]

            break

    return x_if_vap, x_if_liq


def get_bulk_positions(x_if_vap, x_if_liq, lv, ll):

    x_bulk_vap = x_if_vap + lv

    x_bulk_liq = x_if_liq - ll

    return x_bulk_vap.values[0], x_bulk_liq.values[0]


def get_fitted_x(x_bulk_vap, x_bulk_liq, binwidth, roundto):

    x_fit_all = np.round(np.arange(x_bulk_liq, x_bulk_vap, binwidth),roundto)

    print(len(x_fit_all))

    return x_fit_all

def smooth_profile(data, df_smoothed, x_fit_all):


    cs = CubicSpline(data.index, data["chemPot_res[0]"],bc_type='clamped')

    print(cs)
    input()
    df_smoothed["pos"] = x_fit_all

    df_smoothed["chemPot_smoothed"] = cs(x_fit_all)

    return df_smoothed

def main():
    
    data,csv_file = import_data()

    x_if_vap, x_if_liq = get_bulk_if_positions(data)

    x_bulk_vap, x_bulk_liq = get_bulk_positions(x_if_vap ,x_if_liq, lv=50, ll= 10)
    
    x_fit_all = get_fitted_x(x_bulk_vap,x_bulk_liq, binwidth=0.5, roundto=3)

    df_smoothed = pd.DataFrame()

    df_smoothed = smooth_profile(data, df_smoothed, x_fit_all)

    print(df_smoothed)
    plt.plot(df_smoothed["pos"], df_smoothed["chemPot_smoothed"])
    plt.show()
    
main()