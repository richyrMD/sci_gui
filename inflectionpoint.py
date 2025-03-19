import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog


def import_data():

    csv_file = filedialog.askopenfilename()

    data = pd.read_csv(csv_file)
    
    return data


def filter_data_to_interface_coordinates(data, m , n):

    data = data[(data["pos"] > m) & (data["pos"] < n)]

    return data


def find_inflection_point(filtered_data, poly_order, min_slope, m ,n):

    x = filtered_data['pos'].values

    y = filtered_data['rho[0]'].values

    sorted_indices = np.argsort(x)

    x, y = x[sorted_indices], y[sorted_indices]

    p = np.polyfit(x, y, poly_order)

    poly_func = np.poly1d(p)

    poly_derivative_1 = np.polyder(poly_func, 1) 

    poly_derivative_2 = np.polyder(poly_func, 2)

    inflection_point_x = np.roots(poly_derivative_2)
    
    inflection_point_x = np.array([x_val for x_val in inflection_point_x if np.isreal(x_val) and m < x_val < n], dtype=float)

    inflection_point_y = np.array([poly_func(x_val) for x_val in inflection_point_x])

    steigungen = np.abs([poly_derivative_1(x_val) for x_val in inflection_point_x])

    filtered_inflection_point_x = list()

    filtered_inflection_point_y = list()

    for x_val, y_val, slope in zip(inflection_point_x, inflection_point_y, steigungen):

        if slope >= min_slope:

            filtered_inflection_point_x.append(x_val)

            filtered_inflection_point_y.append(y_val)

    return filtered_inflection_point_x,filtered_inflection_point_y


def plot(filtered_data, filtered_inflection_point_x, filtered_inflection_point_y, poly_order):
  
    x = filtered_data['pos'].values

    y = filtered_data['rho[0]'].values

    sorted_indices = np.argsort(x)

    x, y = x[sorted_indices], y[sorted_indices]

  
    p = np.polyfit(x, y, poly_order)

    poly_func = np.poly1d(p)

    x_vals = np.linspace(min(x), max(x), 10000)

    y_vals = poly_func(x_vals)

    plt.plot(x, y, 'bo', label='Daten')
    
    plt.plot(x_vals, y_vals, 'r-', label=f'Polynom (Ordnung {poly_order})')

    plt.plot(filtered_inflection_point_x, filtered_inflection_point_y, 'go', markersize=10, label='Gefilterte Wendepunkte')

    plt.legend()

    plt.xlabel('Ort')

    plt.ylabel('Dichte')

    plt.title('Polynom-Interpolation mit Wendepunkten (min. Steigung)')

    plt.show()


def extend_dataframe_w_interface_information(data, filtered_inflection_point_x, filtered_inflection_point_y, scenario):

    data["INTERFACE_METHOD_SHARP"] = False

    data["INTERFACE_METHOD_SPACIAL"] = False

    #sharp method

    nearest_idx_x = (data["pos"] - filtered_inflection_point_x).abs().idxmin()

    data.at[nearest_idx_x, "INTERFACE_METHOD_SHARP"] = True

    #spacial method

    for i in range(50,100,1):
        density_vap  = data["rho[0]"][nearest_idx_x + i]



    
def main():

    scenario = "" #hflux, evap
    m, n = 458,468
    
    data = import_data()

    filtered_data = filter_data_to_interface_coordinates(data, m, n)

    filtered_inflection_point_x, filtered_inflection_point_y = find_inflection_point(filtered_data, poly_order=100, min_slope=0.1,m=m,n=n)

    #plot(filtered_data, filtered_inflection_point_x, filtered_inflection_point_y, poly_order = 103)

    extend_dataframe_w_interface_information(data,filtered_inflection_point_x,filtered_inflection_point_y, scenario)
    

main()



