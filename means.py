import pandas as pd
import tkinter as tk
from tkinter import filedialog
pd.set_option('display.max_rows', None)
def load_and_calculate_average():
    # Tkinter-Fenster für Dateiauswahl
    root = tk.Tk()
    root.withdraw()  # Verstecke das Hauptfenster
    file_path = filedialog.askopenfilename(title="Datei auswählen")
    print(file_path)
    
    if not file_path:
        print("Keine Datei ausgewählt.")
        return None
    
    try:
        # Datei einlesen (automatische Trennung nach Leerzeichen oder Tab)
        df = pd.read_csv(file_path, delim_whitespace=True)
        
        # Durchschnitt der Spalten berechnen
        mean_values = df.mean()
        
        # Ergebnis als DataFrame zurückgeben
        result_df = pd.DataFrame(mean_values, columns=['Durchschnitt'])
        print(result_df)
        return result_df
    
    except Exception as e:
        print(f"Fehler beim Einlesen der Datei: {e}")
        return None

# Funktion aufrufen
if __name__ == "__main__":
    load_and_calculate_average()
