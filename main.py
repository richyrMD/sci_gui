import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import filedialog, simpledialog
from static_functions import *
matplotlib.use('TkAgg')

class SettingsWindow(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title("Einstellungen")
        self.geometry("300x400")

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

        tk.Label(self, text="Logx:").pack()
        self.logx_entry = tk.Entry(self)
        self.logx_entry.insert(0, str(parent.plot_settings["log_x"]))
        self.logx_entry.pack()

        tk.Label(self, text="Logy:").pack()
        self.logy_entry = tk.Entry(self)
        self.logy_entry.insert(0, str(parent.plot_settings["log_y"]))
        self.logy_entry.pack()

        tk.Label(self,text="grid_y").pack()
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

        tk.Label(self, text="Mehrfach-Plots (z. B. 1,2,3):").pack()
        self.multi_plot_entry = tk.Entry(self)
        self.multi_plot_entry.insert(0, ",".join(map(str, parent.plot_settings["multi_plot"])))
        self.multi_plot_entry.pack()

        tk.Button(self, text="Speichern", command=self.save_settings).pack()

    def save_settings(self):
        self.parent.plot_settings["color"] = self.color_entry.get()
        self.parent.plot_settings["linestyle"] = self.linestyle_entry.get()
        self.parent.plot_settings["linewidth"] = float(self.linewidth_entry.get())
        self.parent.plot_settings["marker"] = self.marker_entry.get()
        self.parent.plot_settings["markersize"] = int(self.markersize_entry.get())
        self.parent.plot_settings["log_x"] = str_bool(self.logx_entry.get())
        self.parent.plot_settings["log_y"] = str_bool(self.logy_entry.get())
        self.parent.plot_settings["grid_y"] = str_bool(self.grid_y_entry.get())
        self.parent.plot_settings["grid_x"] = str_bool(self.grid_x_entry.get())
        self.parent.plot_settings["base_col"] = int(self.base_col_entry.get())
        # Konvertiere Multi-Plot-String in Liste von Listen
        multi_plot_input = self.multi_plot_entry.get()  # Dies könnte ein Textfeld für Gruppenwahl sein
        # Hier nehmen wir an, dass die Eingabe durch Kommas getrennte Zahlen sind
        if multi_plot_input:
            multi_plot = [list(map(int, group.split(','))) for group in multi_plot_input.split(';')]
            self.parent.plot_settings["multi_plot"] = multi_plot
        else:
            self.parent.plot_settings["multi_plot"] = []
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
            "color": "blue",
            "linestyle": "-",
            "linewidth": 1.5,
            "marker": "",
            "markersize": 5,
            "log_x": False,
            "log_y": False,
            "grid_x": False,
            "grid_y":False,
            "base_col":0,
            "multi_plot": []
        }
        self.load_data()
        self.init_plot()

    def load_data(self, reload=False):
        if not hasattr(self, "file_path") or not self.file_path or reload:
            root = tk.Tk()
            root.withdraw()
            self.file_path = filedialog.askopenfilename(filetypes=[("DAT files", "*.dat"), ("All files", "*.*")])

        with open(self.file_path, 'r') as f:
            headers = f.readline().strip().split()

        self.data = np.loadtxt(self.file_path, skiprows=1)

        self.x = self.data[:, self.plot_settings["base_col"]]
        self.x_label = headers[self.plot_settings["base_col"]]

        self.y_values = np.delete(self.data, self.plot_settings["base_col"], axis=1)
        self.y_labels = [label for i, label in enumerate(headers) if i != self.plot_settings["base_col"]]

        self.num_profiles = self.y_values.shape[1]

    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)
        self.plot_profile()
        self.button_frame = ButtonFrame(self)
        self.fig.canvas.mpl_connect("pick_event", self.on_pick)
        plt.show()

    def plot_profile(self):
        self.ax.clear()

        # Prüfen, ob `multi_plot`-Einstellung gesetzt wurde
        multi_groups = self.plot_settings.get("multi_plot", [])

        # Nur eine Gruppe von Profilen wird angezeigt, wenn `current_index` zu dieser Gruppe gehört
        selected_profiles = None
        for group in multi_groups:
            if self.current_index in group:
                selected_profiles = group
                break

        # Falls eine Gruppe existiert, plotte diese Profile zusammen
        if selected_profiles:
            for idx in selected_profiles:
                self.ax.plot(self.x, self.y_values[:, idx], label=self.y_labels[idx],
                             color=self.plot_settings["color"], linestyle=self.plot_settings["linestyle"],
                             linewidth=self.plot_settings["linewidth"],
                             marker=self.plot_settings["marker"],
                             markersize=self.plot_settings["markersize"])
            self.ax.set_title(", ".join([self.y_labels[idx] for idx in selected_profiles]))
        else:
            # Falls keine Gruppen eingestellt sind, plotte nur das aktuelle Profil
            self.ax.plot(self.x, self.y_values[:, self.current_index], label=self.y_labels[self.current_index],
                         color=self.plot_settings["color"], linestyle=self.plot_settings["linestyle"],
                         linewidth=self.plot_settings["linewidth"],
                         marker=self.plot_settings["marker"],
                         markersize=self.plot_settings["markersize"])
            self.ax.set_title(self.y_labels[self.current_index])

        self.ax.set_xlabel(self.x_label)
        self.ax.legend()
        self.ax.grid(self.plot_settings["grid_y"], axis='y')
        self.ax.grid(self.plot_settings["grid_x"], axis='x')

        # Log-Skalierung für X-Achse, falls gewünscht
        if self.plot_settings["log_x"] and np.all(self.x > 0):  # Stellen sicher, dass X nur positive Werte enthält
            self.x_min = min(self.x)
            self.x_max = max(self.x)
            self.ax.set_xscale("log")
            self.ax.set_xlim(left=self.x_min / 1.1, right=self.x_max * 1.1)
        else:
            self.x_min = min(self.x)
            self.x_max = max(self.x)
            self.x_range = self.x_max - self.x_min
            x_buffer = 0.1 * self.x_range if self.x_range > 0 else 1
            self.ax.set_xlim(left=self.x_min, right=self.x_max)
            self.ax.set_xticks(np.linspace(self.x_min, self.x_max, 10))

        # Log-Skalierung für Y-Achse, falls gewünscht
        # Wir müssen die Y-Werte aus allen ausgewählten Profilen kombinieren, um eine globale Skalierung zu finden
        y_min, y_max = np.inf, -np.inf
        for idx in selected_profiles or [self.current_index]:
            y_values_for_profile = self.y_values[:, idx]
            positive_y_values = y_values_for_profile[y_values_for_profile > 0]  # Nur positive Werte
            if len(positive_y_values) > 0:
                y_min = min(y_min, min(positive_y_values))
                y_max = max(y_max, max(positive_y_values))
            else:
                y_min = min(y_min, min(y_values_for_profile))
                y_max = max(y_max, max(y_values_for_profile))

        self.y_range = y_max - y_min
        self.y_buffer = 0.1 * self.y_range if self.y_range > 0 else 1

        if self.plot_settings["log_y"] and y_min > 0:  # Sicherstellen, dass keine null- oder negativen Werte existieren
            self.ax.set_yscale("log")
            self.ax.set_ylim(bottom=y_min / 1.1, top=y_max * 1.1)
        else:
            self.ax.set_ylim(bottom=y_min - self.y_buffer, top=y_max + self.y_buffer)
            self.ax.set_yticks(np.linspace(y_min, y_max, 10))

        plt.draw()

    def on_pick(self, event):
        if isinstance(event.artist, plt.Text):
            new_label = simpledialog.askstring("Titel ändern", "Neuen Titel eingeben:",
                                               initialvalue=self.y_labels[self.current_index])
            if new_label:
                self.y_labels[self.current_index] = new_label
                self.plot_profile()

    def next_profile(self):
        multi_groups = self.plot_settings.get("multi_plot", [])

        # Prüfen, ob der aktuelle Index Teil einer Gruppe ist
        selected_group = None
        for group in multi_groups:
            if self.current_index in group:
                selected_group = group
                break

        # Falls eine Gruppe existiert, gehe zum nächsten Index, aber überspringe alle Profil-Indizes der aktuellen Gruppe
        if selected_group:
            group_size = len(selected_group)
            # Erhöhe den current_index um die Größe der Gruppe
            if self.current_index + group_size < self.num_profiles:
                self.current_index += group_size
        else:
            # Wenn keine Gruppe existiert, gehe einfach zum nächsten Profil
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

