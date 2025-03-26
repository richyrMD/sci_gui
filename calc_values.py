import pandas as pd 
import numpy as np
from tkinter import filedialog
from ljts_v2 import g_ms22PeTS
#pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def import_data():

    csv_file = filedialog.askopenfilename()

    #csv_file = "/home/richy/Schreibtisch/post-processing/sci_gui/testing/profile_means_inflectionpoint/test_01/20250318_145653_means.csv"

    data = pd.read_csv(csv_file)
    
    return data,csv_file


def reduce_data_to_relevant(data):
    
    data.rename(columns={'jEF_y[0]': 'je'}, inplace=True)

    data["jp"] = data["v_y[0]"] * data["rho[0]"]

    data["ekin"] = data["v_y[0]"]*data["v_y[0]"]*0.5

    data["h"] = data["epot[0]"] + data["p[0]"]/data["rho[0]"] - data["T[0]"] + 5/2 * data["T[0]"]
    
    data["q"] = data["je"] * (data["h"] + data["ekin"])

    data["mu"] = g_ms22PeTS(data["chemPot_res[0]"], T=data["T[0]"], rho=data["rho[0]"])

    data = data[["pos","rho[0]","T[0]","epot[0]","p[0]","mu","T_x[0]","T_y[0]","T_z[0]","v_y[0]",
                 "p_x[0]","p_y[0]","p_z[0]","je","jp","ekin","h","q","INTERFACE_METHOD_SHARP","INTERFACE_METHOD_SPACIAL"]]
    
    #print(data)
    #input()
    return data

def get_gradient_positions(data, ll, lv):
    
    interface_edges  = data.loc[data["INTERFACE_METHOD_SPACIAL"] == "True"]

    liq_if_edge = interface_edges.iloc[[0]]

    vap_if_edge = interface_edges.iloc[[1]]

    bulk_liq = data.loc[data["pos"] == liq_if_edge["pos"].values[0] - ll]

    bulk_vap = data.loc[data["pos"] == vap_if_edge["pos"].values[0] + lv]
    
    return liq_if_edge["pos"].values[0], vap_if_edge["pos"].values[0], bulk_liq["pos"].values[0], bulk_vap["pos"].values[0]


def calc_variables(data, liq_if_edge,vap_if_edge, liq_bulk, vap_bulk):

    q_v_const = round(data.loc[(data["pos"] >= vap_if_edge) & (data["pos"] <= vap_bulk), "q"].mean(), 8)
    
    jp_const = round(data.loc[(data["pos"] >= vap_if_edge) & (data["pos"] <= vap_bulk), "jp"].mean(), 8)
    
    je_const = round(data.loc[(data["pos"] >= vap_if_edge) & (data["pos"] <= vap_bulk), "je"].mean(), 8)
    
    h_v = data.loc[data["pos"] == vap_if_edge, "h"].values[0]

    h_l = data.loc[data["pos"] == liq_if_edge, "h"].values[0]
    
    T_v = data.loc[data["pos"] == vap_if_edge, "T[0]"].values[0]  # Temperature at right boundary of IF
    T_l = data.loc[data["pos"] == liq_if_edge, "T[0]"].values[0]  # Temperature at left boundary of IF
 
    mu_v = data.loc[data["pos"] == vap_if_edge, "mu"].values[0]
    mu_l = data.loc[data["pos"] == liq_if_edge, "mu"].values[0]
    
    T_if = data.loc[data["pos"] == 0.0, "T[0]"].values[0]  # Interface temperature (at position = 0)
    
    rho_v = data.loc[data["pos"] == vap_if_edge, "rho[0]"].values[0]

    print(q_v_const,jp_const,je_const)

    input()

    print(h_v,h_l,T_v,T_l, mu_v, mu_l, T_if, rho_v)
    
    input()
    
    Xq_v = (1/T_v) - (1/T_l)
    Xu_v = ((mu_l/T_l) - (mu_v/T_v)) + h_v * ((1/T_v) - (1/T_l))
    
    R_22_v_direct = Xq_v / q_v_const  # r_qq
    R_21_v_direct = np.nan            # r_qu
    R_12_v_direct = Xu_v / q_v_const  # r_uq
    R_11_v_direct = np.nan            # r_uu

    print(R_22_v_direct, R_12_v_direct)

    input()
    
def export_data(data, csv_file):

    data.to_csv(csv_file, index=False)


def main():

    data, csv_file = import_data()

    data = reduce_data_to_relevant(data)

    liq_if_edge, vap_if_edge, liq_bulk , vap_bulk = get_gradient_positions(data, ll = 10, lv = 50)

    calc_variables(data, liq_if_edge, vap_if_edge, liq_bulk, vap_bulk)
    print(liq_if_edge,vap_if_edge,liq_bulk,vap_bulk)
    input()
    #export_data(data,csv_file)
    

main()