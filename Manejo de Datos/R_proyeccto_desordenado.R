
# 2. Extrae nombres de columna y sus etiquetas (labels)
var_names  <- names(df_casen)
var_labels <- sapply(df_casen, function(x) attr(x, "label"))

# 3. Combínalos en un data.frame
info_vars <- data.frame(
  nombre_columna   = var_names,
  etiqueta         = unname(var_labels),
  stringsAsFactors = FALSE
)

# 4. Imprime el resultado
print(info_vars)


write.table(
  info_vars,
  file         = "nombres columnas casen.xls",
  sep          = "\t",
  row.names    = FALSE,
  col.names    = TRUE,
  quote        = FALSE,
  fileEncoding = "latin1"     # <- clave para que Excel Windows muestre bien los acentos
)

cols <- c(
  "id_vivienda", "folio", "id_persona", "region", "area", "estrato",
  "expr", "expr_osig",
  "educ", "esc", "nse", "ypch", "ytotcorh", "qautr",
  "edad", "sexo", "pueblos_indigenas", "tipohogar", "activ", "asal", "contrato", "cotiza",
  "pobreza", "li", "lp", "pobreza_multi_4d", "hh_d_hacina", "hh_d_servbas",
  "tot_per_h", "n_nucleos", "men18c", "may60c"
)
casen_chico_1 <- subset(df_casen, select = cols)


library(dplyr)

# 2. Extraer sólo folio, id_persona y comuna de tu df de geografía
geo <- Base_de_datos_provincia_y_comuna_Casen_2022_STATA %>%
  select(folio, id_persona, comuna)

# 3. Hacer el left join con tu df reducido de CASEN
casen_geo <- casen_chico_1 %>%
  left_join(geo, by = c("folio", "id_persona"))

# Guardar como CSV (valores separados por comas)
write.table(
  casen_geo,
  file      = "casen_geo.xls",
  row.names = FALSE,     # sin índices de fila
  fileEncoding = "UTF-8"  # para conservar tildes y eñes
)

# 1) Tab‐delimitado “.xls” (Excel lo abre bien)
write.table(
  casen_geo,
  file         = "casen_geo.xls",
  sep          = "\t",
  row.names    = FALSE,
  col.names    = TRUE,
  quote        = FALSE,
  fileEncoding = "UTF-8"     # <- clave para que Excel Windows muestre bien los acentos
)
