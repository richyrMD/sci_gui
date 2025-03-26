import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import filedialog, simpledialog
from static_functions import *
import pandas as pd

matplotlib.use('TkAgg')


class SettingsWindow(tk.Tk):
    def __init__(self, parent):

        super().__init__()

        self.parent = parent

        self.title("Einstellungen")

        self.geometry("300x800")

        tk.Label(self, text="Farbe:").pack()

        self.color_entry = tk.Entry(self)

        self.color_entry.insert(0, parent.plot_settings["color"])

        self.color_entry.pack()

        tk.Label(self, text="Linienstil:").pack()

        self.linestyle_entry = tk.Entry(self)

        self.linestyle_entry.insert(0, parent.plot_settings["linestyle"])

        self.linestyle_entry.pack()

        tk.Label(self, text="Linienbreite:").pack()

        self.linewidth_entry = tk.Entry(self)

        self.linewidth_entry.insert(0, str(parent.plot_settings["linewidth"]))

        self.linewidth_entry.pack()

        tk.Label(self, text="Marker:").pack()

        self.marker_entry = tk.Entry(self)

        self.marker_entry.insert(0, parent.plot_settings["marker"])

        self.marker_entry.pack()

        tk.Label(self, text="Markergröße:").pack()

        self.markersize_entry = tk.Entry(self)

        self.markersize_entry.insert(0, str(parent.plot_settings["markersize"]))

        self.markersize_entry.pack()

        tk.Label(self, text="Markerfarbe:").pack()

        self.markercolor_entry = tk.Entry(self)

        self.markercolor_entry.insert(0, str(parent.plot_settings["markercolor"]))

        self.markercolor_entry.pack()

        tk.Label(self, text="Logx:").pack()

        self.logx_entry = tk.Entry(self)

        self.logx_entry.insert(0, str(parent.plot_settings["log_x"]))

        self.logx_entry.pack()

        tk.Label(self, text="Logy:").pack()

        self.logy_entry = tk.Entry(self)

        self.logy_entry.insert(0, str(parent.plot_settings["log_y"]))

        self.logy_entry.pack()

        tk.Label(self, text="grid_y").pack()

        self.grid_y_entry = tk.Entry(self)

        self.grid_y_entry.insert(0, str(parent.plot_settings["grid_y"]))

        self.grid_y_entry.pack()

        tk.Label(self, text="grid_x").pack()

        self.grid_x_entry = tk.Entry(self)

        self.grid_x_entry.insert(0, str(parent.plot_settings["grid_x"]))

        self.grid_x_entry.pack()

        tk.Label(self, text="base_col").pack()

        self.base_col_entry = tk.Entry(self)

        self.base_col_entry.insert(0, str(parent.plot_settings["base_col"]))

        self.base_col_entry.pack()

        tk.Button(self, text="Speichern", command=self.save_settings).pack()

    def save_settings(self):

        self.parent.plot_settings["color"] = self.color_entry.get()

        self.parent.plot_settings["linestyle"] = self.linestyle_entry.get()

        self.parent.plot_settings["linewidth"] = float(self.linewidth_entry.get())

        self.parent.plot_settings["marker"] = self.marker_entry.get()

        self.parent.plot_settings["markersize"] = int(self.markersize_entry.get())

        self.parent.plot_settings["markercolor"] = self.markercolor_entry.get()

        self.parent.plot_settings["log_x"] = str_bool(self.logx_entry.get())

        self.parent.plot_settings["log_y"] = str_bool(self.logy_entry.get())

        self.parent.plot_settings["grid_y"] = str_bool(self.grid_y_entry.get())

        self.parent.plot_settings["grid_x"] = str_bool(self.grid_x_entry.get())

        self.parent.plot_settings["base_col"] = int(self.base_col_entry.get())

        self.parent.load_data(reload=False)

        self.parent.plot_profile()

        self.destroy()


class ButtonFrame:

    def __init__(self, plot_app):

        self.plot_app = plot_app

        self.fig = plot_app.fig

        axprev = plt.axes([0.5, 0.05, 0.1, 0.075])

        axnext = plt.axes([0.61, 0.05, 0.1, 0.075])

        axsettings = plt.axes([0.72, 0.05, 0.18, 0.075])

        self.bnext = Button(axnext, 'Weiter')

        self.bprev = Button(axprev, 'Zurück')

        self.bsettings = Button(axsettings, 'Einstellungen')

        self.bnext.on_clicked(lambda event: self.plot_app.next_profile())

        self.bprev.on_clicked(lambda event: self.plot_app.prev_profile())

        self.bsettings.on_clicked(lambda event: self.plot_app.open_settings())


class PlotApp:

    def __init__(self):

        self.current_index = 0

        self.plot_settings = {
            "color": "dimgray",
            "linestyle": "-.",
            "linewidth": 1.5,
            "marker": "*",
            "markersize": 1,
            "markercolor": "royalblue",
            "log_x": False,
            "log_y": False,
            "grid_x": True,
            "grid_y": True,
            "base_col": 0
        }
        self.load_data()
        self.get_if_position()
        self.init_plot()

    def load_data(self, reload=False):

        if not hasattr(self, "file_path") or not self.file_path or reload:

            root = tk.Tk()

            root.withdraw()

            self.file_path = filedialog.askopenfilename(
                filetypes=[("DAT files", "*.dat"), ("CSV files", "*.csv"), ("All files", "*.*")])
            #self.file_path = "/home/richy/Schreibtisch/run03_noctua_Simon/20250323_192010_means.csv"

        file_extension = self.file_path.split('.')[-1].lower()

        if file_extension == 'csv':

            self.data = pd.read_csv(self.file_path)

            self.headers = self.data.columns.tolist()

            self.x = self.data.iloc[:, self.plot_settings["base_col"]]

            self.x_label = self.headers[self.plot_settings["base_col"]]

            self.y_values = self.data.drop(columns=[self.x_label]).values

            self.y_labels = [label for i, label in enumerate(self.headers) if i != self.plot_settings["base_col"]]

            self.num_profiles = self.y_values.shape[1]

        elif file_extension == 'dat':

            with open(self.file_path, 'r') as f:

                headers = f.readline().strip().split()

            self.data = np.loadtxt(self.file_path, skiprows=1)

            self.x = self.data[:, self.plot_settings["base_col"]]

            self.x_label = headers[self.plot_settings["base_col"]]

            self.y_values = np.delete(self.data, self.plot_settings["base_col"], axis=1)

            self.y_labels = [label for i, label in enumerate(headers) if i != self.plot_settings["base_col"]]

            self.num_profiles = self.y_values.shape[1]

        else:

            raise ValueError(f"Unsupported file extension: {file_extension}")

    def init_plot(self):

        self.fig, self.ax = plt.subplots()

        plt.subplots_adjust(bottom=0.3)

        self.plot_profile()

        self.button_frame = ButtonFrame(self)

        self.fig.canvas.mpl_connect("pick_event", self.on_pick)

        plt.show()

    def get_if_position(self):
        
        
        self.rows_with_true = np.where(self.y_values[:,-2] == True)[0]
        self.if_pos = self.x[self.rows_with_true]
        
        
    def plot_profile(self):

        self.ax.clear()

        self.ax.plot(self.x, self.y_values[:, self.current_index], label=self.y_labels[self.current_index],
                     color=self.plot_settings["color"], linestyle=self.plot_settings["linestyle"],
                     linewidth=self.plot_settings["linewidth"], marker=self.plot_settings["marker"],
                     markersize=self.plot_settings["markersize"], markerfacecolor=self.plot_settings["markercolor"],
                     markeredgecolor=self.plot_settings["markercolor"])

        self.ax.set_ylabel(self.y_labels[self.current_index])

        self.ax.set_xlabel(self.x_label)

        self.ax.set_title(self.y_labels[self.current_index], picker=True)

        self.ax.legend()

        self.ax.grid(self.plot_settings["grid_y"], axis='y')

        self.ax.grid(self.plot_settings["grid_x"], axis='x')

        self.ax.axvline(x=0, linestyle="--", color="purple", linewidth=1)


        if self.plot_settings["log_x"] and np.any(self.x > 0):

            self.x_min = np.nanmin(self.x[self.x > 0])

            self.x_max = np.nanmax(self.x)

            self.ax.set_xscale("log")

            self.ax.set_xlim(left=self.x_min / 1.1, right=self.x_max * 1.1)

        else:

            self.x_min = np.nanmin(self.x)

            self.x_max = np.nanmax(self.x)

            self.x_range = self.x_max - self.x_min

            x_buffer = 0.1 * self.x_range if self.x_range > 0 else 1

            self.ax.set_xlim(left=self.x_min, right=self.x_max)

            self.ax.set_xticks(np.linspace(self.x_min, self.x_max, 10))

        self.positive_y_values = self.y_values[:, self.current_index][self.y_values[:, self.current_index] > 0]

        self.y_min = np.nanmin(self.positive_y_values) if self.plot_settings["log_y"] and len(
            self.positive_y_values) > 0 else np.nanmin(
            self.y_values[:, self.current_index])

        self.y_max = np.nanmax(self.y_values[:, self.current_index])

        self.y_range = self.y_max - self.y_min

        self.y_buffer = 0.1 * self.y_range if self.y_range > 0 else 1

        if self.plot_settings["log_y"] and len(self.positive_y_values) > 0:

            self.ax.set_yscale("log")

            self.ax.set_ylim(bottom=self.y_min / 1.1, top=self.y_max * 1.1)

        else:

            self.ax.set_ylim(bottom=self.y_min - self.y_buffer, top=self.y_max + self.y_buffer)

            self.ax.set_yticks(np.linspace(self.y_min, self.y_max, 10))

        plt.draw()

    def on_pick(self, event):

        if isinstance(event.artist, plt.Text):

            new_label = simpledialog.askstring("Titel ändern", "Neuen Titel eingeben:",
                                               initialvalue=self.y_labels[self.current_index])

            if new_label:

                self.y_labels[self.current_index] = new_label

                self.plot_profile()

    def next_profile(self):

        if self.current_index < self.num_profiles - 1:

            self.current_index += 1

            self.plot_profile()

    def prev_profile(self):

        if self.current_index > 0:

            self.current_index -= 1

            self.plot_profile()

    def open_settings(self):

        SettingsWindow(self)


if __name__ == "__main__":

    PlotApp()
