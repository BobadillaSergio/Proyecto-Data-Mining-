import os
import pandas as pd

# 1. Ruta al archivo de entrada
base = os.getcwd()
ruta_entrada = os.path.join(base, 'Datos', 'casen_geo.xls.xlsx')

# 2. Carga de datos
df = pd.read_excel(ruta_entrada, sheet_name='casen_geo')

# 3. Limpieza de la columna 'comuna'
df['comuna'] = (
    pd.to_numeric(df['comuna'], errors='coerce')
      .fillna(0)
      .astype(int)
      .astype(str)
      .str.zfill(5)
)

# 4. Mapa de comunas D20
comunas_d20 = {
    '08101': 'Concepción',
    '08102': 'Coronel',
    '08103': 'Chiguayante',
    '08104': 'Florida',
    '08105': 'Hualqui',
    '08107': 'Penco',
    '08108': 'San Pedro de la Paz',
    '08109': 'Santa Juana',
    '08110': 'Talcahuano',
    '08111': 'Tomé',
    '08112': 'Hualpén'
}

# 5. Filtrado y nombrado
df_d20 = df[df['comuna'].isin(comunas_d20)].copy()
df_d20['comuna_nombre'] = df_d20['comuna'].map(comunas_d20)

# 6. Informar cantidad
print(f"Registros en D20: {len(df_d20)}")

# 7. Rutas de salida
ruta_xlsx = os.path.join(base, 'Datos', 'casen_d20.xlsx')

# 8. Exportar a Excel (reemplaza si ya existe)
with pd.ExcelWriter(ruta_xlsx, engine='openpyxl') as writer:
    df_d20.to_excel(writer, index=False, sheet_name='Distrito20')

print(f"Archivos guardados en:\n  {ruta_xlsx}")