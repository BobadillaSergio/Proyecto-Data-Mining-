import os
import pandas as pd

# Paths
datos_dir = os.path.join("Datos")
path_csv = os.path.join(datos_dir, "votos_mesa_con_casen.csv")
path_excel = os.path.join(datos_dir, "votos_mesa_con_casen.xlsx")

# Cargar CSV
df = pd.read_csv(path_csv)

# Columnas a eliminar
columnas_a_eliminar = [
    "participa_fuerza_trabajo",
    "pobreza_multidimensional",
    "autoidentidad_indigena",
    "tipo_hogar",
    "total_personas_hogar",
    "genero"
]

# Eliminar columnas
df_depurado = df.drop(columns=columnas_a_eliminar, errors="ignore")

# Sobrescribir archivos originales
df_depurado.to_csv(path_csv, index=False)
df_depurado.to_excel(path_excel, index=False)

print("Archivos depurados guardados exitosamente:")
print("CSV:", path_csv)
print("Excel:", path_excel)
