import os
import pandas as pd

# Ruta de entrada y salida
base = os.getcwd()
ruta_in  = os.path.join(base, 'Datos', 'votos_mesa_con_bloques.xlsx')
ruta_out = os.path.join(base, 'Datos', 'votos_mesa_tidy.xlsx')

# Carga
df = pd.read_excel(ruta_in)

# Limpieza de nombres (opcional)
df.columns = df.columns.str.strip()

# Columnas de CASEN que quieres mantener antes de la parte de mesa
casen_cols = [
    'zona_urbano_rural',
    'nivel_educativo',
    'nivel_socioeconomico',
    'edad_persona'
]

# Columnas que identifican cada mesa
mesa_cols = [
    'codigo_comuna',
    'Circ. Electoral',
    'Local',
    'Nro. Mesa',
    'Electores'
]

# Agrupar votos por mesa y bloque en formato “tidy”
tidy = (
    df
    .groupby(mesa_cols + casen_cols + ['bloque'], dropna=False)['votos']
    .sum()
    .reset_index()
    .rename(columns={'votos': 'votos_bloque'})
)

# Reordenar columnas: primero CASEN, luego identificación de mesa, luego bloque y votos
ordered_cols = casen_cols + mesa_cols + ['bloque', 'votos_bloque']
tidy = tidy[ordered_cols]

# Guardar el resultado
tidy.to_excel(ruta_out, index=False)

print(f"Archivo tidy guardado en: {ruta_out}")
