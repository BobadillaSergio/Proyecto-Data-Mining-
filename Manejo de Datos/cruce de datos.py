import os
import pandas as pd
import numpy as np

# Paths relativos al entorno de carpetas que mostraste
datos_dir = os.path.join( "Datos")
path_votos = os.path.join(datos_dir, "8 Region del Biobio_diputados_tricel.xlsx")
path_casen = os.path.join(datos_dir, "casen_d20_reducido.csv")

# Cargar datos
votos_df = pd.read_excel(path_votos)
casen_df = pd.read_csv(path_casen)

# Normalizar todo!!
def normalizar_nombre(nombre):
    return str(nombre).strip().upper().replace("É", "E").replace("Á", "A").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")

votos_df["Comuna"] = votos_df["Comuna"].apply(normalizar_nombre)
casen_df["nombre_comuna"] = casen_df["nombre_comuna"].apply(normalizar_nombre)


# Agregación CASEN por comuna usando pesos de expansión (representatividad)
def weighted_avg(df, col, weight):
    return np.average(df[col], weights=df[weight])

# Lista de columnas CASEN a agregar (puedes modificar)
variables_a_agregar = [
    "zona_urbano_rural",          # area
    "nivel_educativo",            # educ
    "nivel_socioeconomico",       # nse
    "ingreso_total_hogar",        # ytotcorh
    "edad_persona",               # edad
    "genero",                     # sexo
    "autoidentidad_indigena",     # pueblos_indigenas
    "tipo_hogar",                 # tipohogar
    "total_personas_hogar",       # tot_per_h
    "participa_fuerza_trabajo",   # activ
    "pobreza_multidimensional",   # pobreza_multi_4d
    "pobreza_ingreso"             # pobreza
]


# Agregar usando representatividad
casen_agregado = casen_df.groupby("nombre_comuna").apply(
    lambda x: pd.Series({
        var: weighted_avg(x, var, "representatividad") for var in variables_a_agregar
    })
).reset_index()

# Cruce: proyectar las variables comunales a cada mesa de esa comuna
votos_enriquecido = votos_df.merge(
    casen_agregado,
    left_on="Comuna",
    right_on="nombre_comuna",
    how="left"
)

# Guardar archivo final
path_output = os.path.join(datos_dir, "votos_mesa_con_casen.csv")
votos_enriquecido.to_csv(path_output, index=False)

path_output_excel = os.path.join(datos_dir, "votos_mesa_con_casen.xlsx")
votos_enriquecido.to_excel(path_output_excel, index=False)


print("Cruce completado. Archivo guardado en:", path_output)
