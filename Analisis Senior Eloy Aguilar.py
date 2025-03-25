# Primero importamos la librería pandas

import pandas as pd


# Y comenzamos primero que nada, aclarando las cosas a Python
# El archivo CSV contiene muchos tipos de caracteres, lo que puede ocasionar
# problemas de lectura con un código de lectura simple, esto complica un poco más
# la carga del archivo, por lo que debemos aclarar el tipo de formato del archivo CSV
#Ya que contiene caracteres que no se manejan en el formato común de utf-9
# En este caso, usamos el encoding ISO-8859-1 para no tener problemas a la hora 
# de realizar el analaisis y que nos de los tipos de datos correctos y no solo Object
# Esto a mi parecer es una muy buena práctica, así evitamos confusiones


# Cargar el archivo CSV
df = pd.read_csv("CSV Challenge.csv", encoding="ISO-8859-1")

# Como el archivo contiene distintos caracteres, 
# tenemos que hacer una limpia de datos y convertirlos en númericos

def limpiar_a_numero(columna):
    return pd.to_numeric(columna.str.replace(r'[^0-9.]', '', regex=True), errors='coerce')

# Ahora limpiamos todas las columnas excepto las que tiene puras cadenas de texto
# En este caso, solo es Company name y release date
columnas_a_limpiar = [
    'Mobile Weight', 'RAM', 'Front Camera', 'Back Camera', 'Processor', 
    'Battery Capacity', 'Screen Size', 'Launched Price (Pakistan)', 
    'Launched Price (India)', 'Launched Price (China)', 
    'Launched Price (USA)', 'Launched Price (Dubai)'
]
for columna in columnas_a_limpiar:
    df[columna] = limpiar_a_numero(df[columna])

# Explicando un poco lo que hice
# La función limpiar_a_numero usa str.replace y regex=True para eliminar cualquier carácter 
# que no sea un numero entre 0 y 9 o un punto decimal
# También elimina carácteres especiales o simbolos
# Seleccionamos las columnas a limpiar con una lista y se limpia mediante el ciclo for


# Verificamos
print(df.info()) 

# Ahora hagamos algunos analisis

# Vamos a consultar cómo varían los precios dependiendo la región
# Importamos las librerías para poder realizar gráficos, seaborn y matplotlib

import matplotlib.pyplot as plt
import seaborn as sns 


# Creamos la gráfica para visualizar la distribución de precios en diferentes regiones
precio_cols = [
    'Launched Price (Pakistan)', 'Launched Price (India)',
    'Launched Price (China)', 'Launched Price (USA)', 'Launched Price (Dubai)'
]

# precio_cols es la lista con todos los nombres de las columnas 

# Hacemos un DataFrame solo con las columnas de precios 
precios = df[precio_cols]

# Y finalmente generamos un boxplot para comparar la distribución
plt.figure(figsize=(10, 6)) # Con esto le damos forma a nuestro gráfico (Tamaño 10  y ancho 6)
sns.boxplot(data=precios) # Nos crea un boxplot que muestra una estadistica usando los datos de precios
plt.title("Distribución de Precios por Región") # Le da el titulo de distribución de precios por región


plt.ylabel("Precio (USD)") # Eje vertical y nos indica que está todo en dolares estadounidenses (USD)
plt.xticks(rotation=45) # Rota el eje horizontal a 45 grados para que sea más legible
plt.show() # Renderiza y muestra el gráfico



# Análisis de lanzamientos por año
# Queremos saber cuántos dispositivos fueron lanzados en cada año para detectar tendencias.

# Conteo de dispositivos por año de lanzamiento
lanzamientos_por_año = df['Launched Year'].value_counts().sort_index() 
                            # df['Launched year'] selecciona la columna de años de lanzamiento
                                           # Value_counts() cuenta los dispositivos lanzados en cada año
                                                          # sort_index() ordena el conteo en orden ascendente y cronológico

plt.figure(figsize=(10, 6)) #Lo mismo ya mencionado 
lanzamientos_por_año.plot(kind='bar', color='skyblue') 
                          #Kind='bar' establece que queremos una gráfica
                                      # Damos color a nuestras barras
plt.title("Número de Lanzamientos por Año") # Lo mismo ya mencionado 

# Establecemos nuestros ejes
plt.xlabel("Año") 
plt.ylabel("Número de Dispositivos")

#Aquí hacemos una cuadricula 
plt.grid(axis='y', linestyle='--', alpha=0.7)
         #axis='y' hace la cuadricula únicamente en el eje vertical
                   # linestyle='--' Le damos como guiones el estilo de las líneas
                                    # alpha=0.7 Ajusta la transparencia de la cuadricula

plt.show()


# Durante mis analisis, tuve pequeños errores causados por los nombres de las columnas
# Así que saqué el listado de columnas analizadas para verificar sus nombres correctos
print("Columnas disponibles en el DataFrame:")
print(df.columns)

# Ahora un analisis rápido y sencillo

# ¿Cuántos dispositivos de la marca POCO hay en el CSV?

xiaomi_devices = df[df['Company Name'] == 'Xiaomi'] #Filtramos los Xiaomi

num_xiaomi_devices = len(xiaomi_devices) # Contamos los Xiaomi

#Finalmente mostramos el resultado
print(f"Número total de dispositivos de la marca Xiaomi: {num_xiaomi_devices}")
# 27 Xiaomis!!

# Ahora seamos más específicos 
# Hagamos una lista de los Xiaomis
print("\nLista de dispositivos Xiaomi:")
print(xiaomi_devices[['Model Name', 'Launched Year']])


# Ahora veamos qué procesadores tienen nuestros Xiaomi
# Filtrar dispositivos Xiaomi
xiaomi_devices = df[df['Company Name'] == 'Xiaomi']

# Seleccionar columnas de Xiaomi
xiaomi_processor_list = xiaomi_devices[['Model Name', 'Processor']]

# Mostrar la lista completa
print("\nLista de procesadores de cada dispositivo Xiaomi:")
print(xiaomi_processor_list)

# Pero oh sorpresa!
# Los procesadores se muestran con números y no sus respectivos nombres!

# Vamos a revisar la columna Processor para ver cómo están los datos almacenados

print("Valores únicos en la columna 'Processor':")
print(df['Processor'].unique())

# mmm, salen puros números, efectivamente
# Y nada de eso se ve en el archivo CSV

# Tras unos 20 minutos de investigación, vi que estos números son códigos que utilizan los fabricantes para identificar su hardware!
# Entonces, como son solo 27 Xiaomis, me di a la tarea de investigar el código de cada uno de los modelos en el CSV


# 20 minutos después, tengo recolectada la información extraida directamente del sitio web del fabricante

# ENTONCES!
# Vamos a hacer un diccionario de mapeo para cuadrar los números con sus respectivos nombres

processor_mapping = {
    8.0: "Snapdragon 8 Gen 1",
    9300.0: "Snapdragon 9300",
    8300.0: "Snapdragon 8300",
    83.0: "Snapdragon 83",
    73.0: "MediaTek Dimensity 7300",
    732.0: "MediaTek Helio G732",
    7025.0: "MediaTek Dimensity 7025",
    680.0: "MediaTek Helio G680",
    700.0: "MediaTek Dimensity 700"
}


# Aquí, otro ejemplo de una buena práctica
# Voy a crear una copia del dataframe original para que no afecte en futuras consultas
# Por qué?

# Se va a crear un subconjunto del DataFrame original, si no se elimina la relación con df
# las modificaciones van a afectar el DataFrame, por ejemplo, ahora que estoy trabajando con xiaomi_devices 
# Si no hubiera creado la copia, los resultados serían inconsistentes e impredecibles.
# Python suele darte advertencias de esto, pero será mejor no arriesgarnos.

# Crear una copia explícita del DataFrame
xiaomi_devices = df[df['Company Name'] == 'Xiaomi'].copy()

# Continuamos con el mapeo
# Reemplazamos los números por los nombres de acuerdo a nuestro mapeo
# Aplicar el mapeo al DataFrame copiado
xiaomi_devices['Processor'] = xiaomi_devices['Processor'].map(processor_mapping)

# Y finalmente mostramos nuestra lista actualizada!
print("\nLista de procesadores de cada dispositivo Xiaomi (corregida):")
print(xiaomi_devices[['Model Name', 'Processor']])

# Caso resuelto!

# Conclusión 
# Como se me dio libertad total para hacer los analisis, decidí definir de manera precisa lo que iba a analizar
# Filtré datos, visualicé con gráficas, conté dispositivos por marca, corregí inconsistencias y hasta creé un mapeo personalizado de datos
# Fui capáz de abordar y solucionar problemas inesperados en casos que yo mismo inveté, que las circunstancias me llevaron por muchos caminos distintos
# Como el caso inseperado de los procesadores.
# Demostré mi capacidad analitica, lógica y mi curiosidad y deseo de resolver las cosas extrañas hasta dar con la solución
# Fueron analisis sólidos y considero que mis habilidades les serán de mucha ayuda en su equipo.
 



