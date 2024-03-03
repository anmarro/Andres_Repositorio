import arcpy

# Establecer el entorno de trabajo
arcpy.env.workspace = r"ruta"

# Obtener una lista de todas las capas de ruta
rutas = arcpy.ListFeatureClasses()

# Ruta al raster reclasificado
reclas = r"raster reclas"

# Ruta y nombre de la tabla de salida de la herramienta Sample
out_table = r"ruta"

# Diccionario que mapea valores a labels
labels = {
    1: "Riesgo muy poco probable",
    2: "Presencia de aludes cuando las condiciones son inestables",
    3: "Mayor ocurrencia de avalanchas. Peligro máximo entre 38 y 39 grados",
    4: "Frecuencia de purgas y pequeñas placas naturales",
    5: "No se suelen acumular espesores. La nieve se purga con frecuencia"
}

# Función para verificar si una ruta intersecta con el raster de pendientes


def intersecta_con_raster(ruta):
    intersecta = False
    # Crear una capa de entidad a partir de la ruta
    capa_ruta = arcpy.management.MakeFeatureLayer(ruta, "capa_ruta")
    # Guardar la capa de entidad en el disco
    ruta_temporal = r"temporal"
    if arcpy.Exists(ruta_temporal):
        arcpy.Delete_management(ruta_temporal)
    arcpy.management.CopyFeatures(capa_ruta, ruta_temporal)
    # Verificar la intersección
    resultado_sample = arcpy.sa.Sample(reclas, ruta_temporal, out_table)
    # Si hay algún resultado, significa que hay intersección
    if int(arcpy.management.GetCount(resultado_sample)[0]) > 0:
        intersecta = True
    return intersecta

# Función para obtener el valor del píxel y mostrar la alerta


def obtener_valor_y_alerta(ruta):
    # Crear una capa de entidad a partir de la ruta
    capa_ruta = arcpy.management.MakeFeatureLayer(ruta, "capa_ruta")
    # Guardar la capa de entidad en el disco
    ruta_temporal = r"temporal"
    if arcpy.Exists(ruta_temporal):
        arcpy.Delete_management(ruta_temporal)
    arcpy.management.CopyFeatures(capa_ruta, ruta_temporal)
    # Realizar la intersección y obtener el valor del píxel
    resultado_sample = arcpy.sa.Sample(reclas, ruta_temporal, out_table)
    campos = ["VALUE"]
    with arcpy.da.SearchCursor(out_table, campos) as cursor:
        for row in cursor:
            valor_pixel = row[0]
            label = labels.get(valor_pixel, "No se ha encontrado el label")
            arcpy.AddWarning(
                f"¡Estás atravesando una zona con el siguiente riesgo: {label}!")


# Recorrer cada ruta
for ruta in rutas:
    if intersecta_con_raster(ruta):
        obtener_valor_y_alerta(ruta)

# Mensaje de finalización
arcpy.AddMessage("Ejecución finalizada.")
