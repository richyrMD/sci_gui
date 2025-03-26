import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog
from scipy.optimize import curve_fit
from get_bulk_values import *
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def import_data():

    csv_file = filedialog.askopenfilename()

    data = pd.read_csv(csv_file)
    
    return data,csv_file


def filter_data_to_interface_coordinates(data, m , n):

    data = data[(data["pos"] >= m) & (data["pos"] < n)]

    return data


def get_discretization(data):

    disc = data["pos"][2] - data["pos"][1]

    return disc


def round_to_discretization(value, disc):

    rounded = round((value/disc)) * disc

    return rounded


def logistic_function(x, C1, C2, x0, tau):
        
    return C1 + (C2 - C1) / (1 + np.exp(-(x - x0) / tau))


def find_inflection_point(data):

    x = data['pos'].values

    y = data['rho[0]'].values

    popt, pcov = curve_fit(logistic_function, x, y)

    if_x = round_to_discretization(popt[2], get_discretization(data))
    
    if_y = data.loc[data["pos"] == if_x, "rho[0]"]

    return if_x, if_y


def plot(data, if_x, if_y):
  
    x = data['pos'].values

    y = data['rho[0]'].values

    popt, pcov = curve_fit(logistic_function, x, y)

    plt.scatter(x, y, s=10)

    plt.scatter(if_x,if_y)

    plt.plot(x, logistic_function(x, *popt), color="red")

    plt.show()


def extend_dataframe_w_interface_information(data, if_x, scenario):

    data.loc[:, "INTERFACE_METHOD_SHARP"] = False

    data.loc[:, "INTERFACE_METHOD_SPACIAL"] = False

    #sharp method

    data.loc[data["pos"] == if_x, "INTERFACE_METHOD_SHARP"] = True

    #spacial method
    bulk_vap,bulk_liq = get_bulk_values_main(data)
    data["RHO_IF_COND_LIQ"] = False
    data["RHO_IF_COND_VAP"] = False
    data["P_IF_COND_LIQ"] = False
    data["P_IF_COND_VAP"] = False
    #data["T_IF_COND_LIQ"] = False
    #data["T_IF_COND_VAP"] = False

    data.loc[abs((data["rho[0]"] - bulk_liq["rho[0]"])/bulk_liq["rho[0]"]) <= 0.01, "RHO_IF_COND_LIQ"] = True
    data.loc[abs((data["rho[0]"] - bulk_vap["rho[0]"])/bulk_vap["rho[0]"]) <= 0.01, "RHO_IF_COND_VAP"] = True

    data['p_xz[0]'] = 0.5*(data['p_z[0]']+data['p_x[0]'])
    data['dp_xzy[0]'] = abs(data['p_xz[0]']-data['p_y[0]'])/abs(data['p_y[0]'])

    data.loc[data["dp_xzy[0]"] <= 0.1,"P_IF_COND_LIQ"] = True
    data.loc[data["dp_xzy[0]"] <= 0.01, "P_IF_COND_VAP"] = True

    '''
    T_liq_fit = np.poly1d(np.polyfit(data[-10:-5].index, data[-10:-5]['T[0]'], 1))(data.index)

    dTliq = data['T[0]'] - T_liq_fit

    T_vap_fit = np.poly1d(np.polyfit(data[15:25].index, data[15:25]['T[0]'], 1))(data.index)

    dTvap = data['T[0]'] - T_vap_fit  # Verwende den gesamten Indexbereich

    data["dTliq"] = abs(dTliq)
    data["dTvap"] = abs(dTvap)

    data.loc[data["dTliq"] <= 0.01,"T_IF_COND_LIQ"] = True
    data.loc[data["dTvap"] <= 0.01, "T_IF_COND_VAP"] = True
    print(data)
    input()
    try:

         print(dTliq[dTliq > 1e-6].index[0])

    except:

        print(-1.0)
    print(dTvap[dTvap > 0.0].index[0])

    #print(data)
    input()
    ###############
    '''

    data['INTERFACE_METHOD_SPACIAL'] = data.apply(lambda row: True if (row['RHO_IF_COND_LIQ'] == False and row['RHO_IF_COND_VAP'] == False and 
                                        row['P_IF_COND_LIQ'] == False and row['P_IF_COND_VAP'] == False and 
                                        0 <= row['pos'] <= 75) else row['INTERFACE_METHOD_SPACIAL'], axis=1)
    
    start = data['INTERFACE_METHOD_SPACIAL'] & ~data['INTERFACE_METHOD_SPACIAL'].shift(1, fill_value=False)
    end = data['INTERFACE_METHOD_SPACIAL'] & ~data['INTERFACE_METHOD_SPACIAL'].shift(-1, fill_value=False)

    # Einen neuen Wert für innere True-Werte setzen (z.B. 'inner_true')
    data['INTERFACE_METHOD_SPACIAL'] = data['INTERFACE_METHOD_SPACIAL'].mask(data['INTERFACE_METHOD_SPACIAL'] & ~start & ~end, 'if')
    
    data.drop(columns=["RHO_IF_COND_LIQ","RHO_IF_COND_VAP","P_IF_COND_LIQ","P_IF_COND_VAP","rho[0]_magnitudes","p_xz[0]","dp_xzy[0]"], inplace=True)

    return data


def norm_to_interface(data):

    data["pos"] = data["pos"] - data.loc[data["INTERFACE_METHOD_SHARP"] == True, "pos"].values[0]

    return data


def export_data(data, csv_file):

    data.to_csv(csv_file, index=False)

 
def main():

    scenario = "" #hflux, evap

    data, csv_file = import_data()

    m,n = 0,len(data)

    disc = get_discretization(data)

    data = filter_data_to_interface_coordinates(data, m, n)

    if_x, if_y = find_inflection_point(data)

    #plot(data, if_x, if_y)

    extend_dataframe_w_interface_information(data, if_x, scenario)

    data = norm_to_interface(data)

    export_data(data, csv_file)
    
main()



