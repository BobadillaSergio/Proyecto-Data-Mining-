import os
import pandas as pd

# Base del proyecto y rutas de archivos
base = os.getcwd()
ruta_entrada = os.path.join(base, 'Datos', 'casen_d20.xlsx')

# 1. Carga de datos
df = pd.read_excel(ruta_entrada)

# 2. Selección de columnas clave
cols = [
    'area',
    'educ',
    'nse',
    'ytotcorh',
    'edad',
    'sexo',
    'pueblos_indigenas',
    'tipohogar',
    'tot_per_h',
    'activ',
    'pobreza_multi_4d',
    'pobreza',
    'comuna',
    'comuna_nombre',
    'expr'
]
df_reducido = df[cols].copy()

# 3. Renombrar columnas a nombres autoexplicativos
rename_map = {
    'area': 'zona_urbano_rural',
    'educ': 'nivel_educativo',
    'nse': 'nivel_socioeconomico',
    'ytotcorh': 'ingreso_total_hogar',
    'edad': 'edad_persona',
    'sexo': 'genero',
    'pueblos_indigenas': 'autoidentidad_indigena',
    'tipohogar': 'tipo_hogar',
    'tot_per_h': 'total_personas_hogar',
    'activ': 'participa_fuerza_trabajo',
    'pobreza_multi_4d': 'pobreza_multidimensional',
    'pobreza': 'pobreza_ingreso',
    'comuna': 'codigo_comuna',
    'comuna_nombre': 'nombre_comuna',
    'expr': 'representatividad'
}
df_reducido.rename(columns=rename_map, inplace=True)

# 4. Ordenar el DataFrame por comuna y edad
df_ordenado = df_reducido.sort_values(by=['nombre_comuna', 'edad_persona'])

# 5. Guardar resultados
ruta_csv = os.path.join(base, 'Datos', 'casen_d20_reducido.csv')
df_ordenado.to_csv(ruta_csv, index=False, encoding='utf-8-sig')

# 6. Confirmación
print(f"Dataset reducido y ordenado guardado en:\n • {ruta_csv}")
