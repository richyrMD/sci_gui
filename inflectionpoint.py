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


def find_inflection_point(data, poly_order, min_slope, m ,n):

    x = data['pos'].values

    y = data['rho[0]'].values

    sorted_indices = np.argsort(x)

    x, y = x[sorted_indices], y[sorted_indices]

    p = np.polyfit(x, y, poly_order)

    poly_func = np.poly1d(p)

    poly_derivative_1 = np.polyder(poly_func, 1) 

    poly_derivative_2 = np.polyder(poly_func, 2)

    inflectionpoint_x = np.roots(poly_derivative_2)
    
    inflectionpoint_x = np.array([x_val for x_val in inflectionpoint_x if np.isreal(x_val) and m < x_val < n], dtype=float)

    inflectionpoint_y = np.array([poly_func(x_val) for x_val in inflectionpoint_x])

    steigungen = np.abs([poly_derivative_1(x_val) for x_val in inflectionpoint_x])

    filtered_inflectionpoint_x = list()

    filtered_inflectionpoint_y = list()

    for x_val, y_val, slope in zip(inflectionpoint_x, inflectionpoint_y, steigungen):

        if slope >= min_slope:

            filtered_inflectionpoint_x.append(x_val)

            filtered_inflectionpoint_y.append(y_val)

    return filtered_inflectionpoint_x,filtered_inflectionpoint_y


def plot(data, filtered_inflectionpoint_x, filtered_inflectionpoint_y, poly_order):
  
    x = data['pos'].values

    y = data['rho[0]'].values

    sorted_indices = np.argsort(x)

    x, y = x[sorted_indices], y[sorted_indices]

  
    p = np.polyfit(x, y, poly_order)

    poly_func = np.poly1d(p)

    x_vals = np.linspace(min(x), max(x), 10000)

    y_vals = poly_func(x_vals)

    plt.plot(x, y, 'bo', label='Daten')
    
    plt.plot(x_vals, y_vals, 'r-', label=f'Polynom (Ordnung {poly_order})')

    plt.plot(filtered_inflectionpoint_x, filtered_inflectionpoint_y, 'go', markersize=10, label='Gefilterte Wendepunkte')

    plt.legend()

    plt.xlabel('Ort')

    plt.ylabel('Dichte')

    plt.title('Polynom-Interpolation mit Wendepunkten (min. Steigung)')

    plt.show()


def main():

    m, n = 452,464

    data = import_data()

    data = filter_data_to_interface_coordinates(data, m, n)

    filtered_inflectionpoint_x, filtered_inflectionpoint_y = find_inflection_point(data, poly_order=103, min_slope=0.1,m=m,n=n)

    plot(data, filtered_inflectionpoint_x, filtered_inflectionpoint_y, poly_order = 103)
    

main()



