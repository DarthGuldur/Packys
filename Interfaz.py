import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog
import pandas as pd

# Leer el archivo CSV
file_path = "CSVChallenge.csv"  # Cambia esto por la ruta de tu archivo
df = pd.read_csv("CSV Challenge.csv", encoding="ISO-8859-1")

# Función para mostrar los Model Name y precios de una marca
def mostrar_modelos_y_precios(marca):
    # Filtrar los dispositivos de la marca seleccionada
    filtered = df[df['Company Name'] == marca]
    if 'Model Name' in df.columns and 'Launched Price (USA)' in df.columns:
        dispositivos = filtered[['Model Name', 'Launched Price (USA)']]  # Seleccionar columnas relevantes
        dispositivos_lista = dispositivos.values.tolist()  # Convertir a lista de pares
        
        if dispositivos.empty:
            messagebox.showinfo("Sin resultados", f"No se encontraron dispositivos para {marca}.")
            return

        # Crear una nueva ventana para los resultados
        resultado_ventana = Toplevel()
        resultado_ventana.title(f"Modelos y Precios de {marca}")

        max_por_columna = 20
        num_columnas = (len(dispositivos_lista) // max_por_columna) + 1
        ancho_ventana = min(300 * num_columnas, 800)  # Máximo ancho de 800
        alto_ventana = min(40 * len(dispositivos_lista), 400)  # Máximo alto de 400
        resultado_ventana.geometry(f"{ancho_ventana}x{alto_ventana}")

        # Función para exportar a CSV
        def exportar_csv():
            # Abrir un cuadro de diálogo para seleccionar la ruta de guardado
            archivo = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv")],
                title="Guardar archivo",
                initialfile=f"{marca}_modelos_precios.csv"
            )
            if archivo:  # Si se seleccionó un archivo
                dispositivos.to_csv(archivo, index=False)
                messagebox.showinfo("Exportar CSV", f"Resultados exportados correctamente a '{archivo}'.")

        # Botón para exportar a CSV (en la parte superior)
        tk.Button(resultado_ventana, text="Exportar a CSV", command=exportar_csv).grid(row=0, column=0, columnspan=num_columnas, pady=10)

        # Mostrar los resultados en columnas (20 por columna, después del botón)
        columnas = [dispositivos_lista[i:i+max_por_columna] for i in range(0, len(dispositivos_lista), max_por_columna)]
        for col_idx, columna in enumerate(columnas):
            for row_idx, (modelo, precio) in enumerate(columna):
                tk.Label(resultado_ventana, text=f"{modelo} - ${precio}", anchor="w").grid(row=row_idx + 1, column=col_idx, padx=10, pady=2)  # "+1" porque el botón está en la fila 0

    else:
        messagebox.showinfo("Error", "Las columnas 'Model Name' o 'Launched Price (USA)' no existen en el DataFrame.")

# Crear la ventana principal
root = tk.Tk()
root.title("Consultas CSV - Exportar Resultados")

# Obtener todas las marcas únicas en la columna Company Name
company_names = df['Company Name'].unique()

# Etiqueta principal
tk.Label(root, text="Consultas CSV por Marca", font=("Arial", 16), bg="white", fg="black").grid(row=0, column=0, columnspan=4, pady=10)

# Crear botones para cada marca
row_index = 1
column_index = 0
for i, marca in enumerate(company_names):
    tk.Button(root, text=f"Modelos y Precios de {marca}", command=lambda m=marca: mostrar_modelos_y_precios(m), bg="white", fg="black").grid(row=row_index, column=column_index, padx=5, pady=5)
    
    column_index += 1
    if column_index > 3:  # Máximo de 4 botones por fila
        column_index = 0
        row_index += 1

# Botón para salir
tk.Button(root, text="Salir", command=root.quit, bg="white", fg="black").grid(row=row_index + 1, column=0, columnspan=4, pady=20)

# Ejecutar la interfaz
root.mainloop()

import sys
import os

# Obtener el directorio donde está el ejecutable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_path, "CSV Challenge.csv")

# Leer el archivo
df = pd.read_csv("CSV Challenge.csv", encoding="ISO-8859-1")

