import os
import pandas as pd

# Definir bloques y excepciones
bloques = {
    'Centro-Derecha': [
        'UNION DEMOCRATA INDEPENDIENTE',
        'INDEPENDIENTE UNION DEMOCRATA INDEPENDIENTE',
        'RENOVACION NACIONAL',
        'EVOLUCION POLITICA',
        'INDEPENDIENTE EVOLUCION POLITICA'
    ],
    'Centro': [
        'PARTIDO DE LA GENTE',
        'PARTIDO RADICAL DE CHILE',
        'INDEPENDIENTE PARTIDO RADICAL DE CHILE',
        'CENTRO UNIDO',
        'INDEPENDIENTE CENTRO UNIDO'
    ],
    'Centro-Izquierda': [
        'PARTIDO SOCIALISTA DE CHILE',
        'INDEPENDIENTE PARTIDO POR LA DEMOCRACIA',
        'PARTIDO DEMOCRATA CRISTIANO'
    ],
    'Izquierda': [
        'PARTIDO ECOLOGISTA VERDE',
        'UNION PATRIOTICA',
        'IGUALDAD',
        'INDEPENDIENTE IGUALDAD',
        'PARTIDO HUMANISTA',
        'INDEPENDIENTE PARTIDO HUMANISTA',
        'INDEPENDIENTE FEDERACION REGIONALISTA VERDE SOCIAL',
        'INDEPENDIENTE CONVERGENCIA SOCIAL',
        'PARTIDO COMUNISTA DE CHILE',
        'REVOLUCION DEMOCRATICA',
        'INDEPENDIENTE REVOLUCION DEMOCRATICA'
    ]
}

partido_a_bloque = {
    partido: bloque
    for bloque, partidos in bloques.items()
    for partido in partidos
}

excepciones = {
    'SERGIO BOBADILLA MUÑOZ':    'Derecha',
    'PAZ CHARPENTIER RAJCEVICH': 'Derecha',
    'FRANCESCA MUÑOZ GONZALEZ':  'Derecha',
}

# Carga de datos
base = os.getcwd()
ruta = os.path.join(base, 'Datos', 'votos_mesa_con_casen.xlsx')
df = pd.read_excel(ruta)

# Normalizar nombres de columnas
df.columns = df.columns.str.strip()
df = df.rename(columns={
    'Comuna': 'codigo_comuna',
    'Partido': 'partido',
    'Candidato': 'candidato',
    'Votos TRICEL': 'votos'
})

# Asegurar que ciertos campos sean strings
df['codigo_comuna'] = df['codigo_comuna'].astype(str).str.zfill(5)
df['partido']      = df['partido'].fillna('').astype(str)
df['candidato']    = df['candidato'].fillna('').astype(str)

# Función para asignar bloque
def asignar_bloque(row):
    c = row['candidato'].strip().upper()
    if c in excepciones:
        return excepciones[c]
    p = row['partido'].strip().upper()
    return partido_a_bloque.get(p, 'Otros')

df['bloque'] = df.apply(asignar_bloque, axis=1)

# Agregar votos por bloque para cada mesa
# agrupamos por los identificadores de mesa
mesa_cols = ['codigo_comuna', 'Circ. Electoral', 'Local', 'Nro. Mesa']
pivot = (
    df
    .groupby(mesa_cols + ['bloque'])['votos']
    .sum()
    .reset_index()
    .pivot(index=mesa_cols, columns='bloque', values='votos')
    .fillna(0)
    .reset_index()
)

# Volver a unir con el DataFrame original para conservar las demás columnas
df_final = df.merge(pivot, on=mesa_cols, how='left')

# Guardar resultado
out_xlsx = os.path.join(base, 'Datos', 'votos_mesa_con_bloques.xlsx')
with pd.ExcelWriter(out_xlsx, engine='openpyxl') as writer:
    df_final.to_excel(writer, index=False, sheet_name='ConBloques')

print(f"Archivo con bloques y votos por mesa guardado en:\n{out_xlsx}")
