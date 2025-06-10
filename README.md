# Proyecto de Minería de Datos (Distrito 20)

Este repositorio contiene los scripts y bases utilizadas para cruzar la
encuesta CASEN con los resultados electorales del Servel en el Distrito 20 de
la Región del Biobío. El objetivo es obtener indicadores socioeconómicos a
nivel de mesa de votación.

## Estructura del repositorio

- **Datos**: hojas de cálculo y archivos CSV generados durante el proceso.
- **Manejo de Datos**: scripts en Python y R para limpiar y unir los datos.
- **GraphicAbstract.png**: esquema gráfico del proyecto.
- **A Futuro**: nota con tareas pendientes.

## Requisitos

- Python 3.x
- `pandas`, `numpy` y `openpyxl`
- (Opcional) R con el paquete `dplyr` para los scripts en R

## Uso

1. Ejecutar `Reorden_casen.py` para filtrar `casen_geo.xls.xlsx` y generar
   `casen_d20.xlsx` con las comunas del Distrito 20.
2. Ejecutar `Orden_casen_d20.py` para reducir columnas y dejar el archivo
   `casen_d20_reducido.csv` listo para análisis.
3. Finalmente, correr `cruce de datos.py` para agregar los datos de CASEN a
   los resultados de votación y producir `votos_mesa_con_casen.csv`.

Los pasos 2 y 3 se resumen en el script `cruce de datos.py` donde se realiza la
agregación comunal utilizando la representatividad como peso:

```python
casen_agregado = casen_df.groupby("nombre_comuna").apply(
    lambda x: pd.Series({
        var: weighted_avg(x, var, "representatividad") for var in variables_a_agregar
    })
).reset_index()
```

## Avance del proyecto

- **Archivos Base**: carga inicial de datos CASEN y Servel, junto con un script
  en R para explorar las etiquetas de las variables.
- **Avance 2**: filtrado de comunas y primer ordenamiento de variables con
  `Reorden_casen.py`.
- **Entrega de avance**: cruce completo de datos y generación de los archivos
  finales `votos_mesa_con_casen.csv` y `votos_mesa_con_casen.xlsx`.

## Pendiente

El archivo `A Futuro` enumera dos tareas principales:

1. Analizar sólo con datos del Servel el comportamiento subterritorial usando
   los locales como referencia, incorporando variables socioeconómicas externas.
2. Evaluar el uso del Censo para complementar la información.

## Licencia

Este proyecto se distribuye sin una licencia explícita. Revisar las fuentes de
datos originales para conocer sus restricciones de uso.
