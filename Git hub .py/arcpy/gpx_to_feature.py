import arcpy
import os
from arcpy.sa import ExtractValuesToPoints

# Espacio de trabajo
arcpy.env.workspace = r""
arcpy.env.overwriteOutput = True

# Lista de capas de puntos
in_point_features = arcpy.ListFeatureClasses("*")

# Ruta del archivo raster de entrada
in_raster = r""

# Ruta del dataset de salida
out_dataset = r""

# Configurar los parámetros de la herramienta
interpolate_values = "NONE"
add_attributes = "VALUE_ONLY"

# Iterar sobre las capas de puntos
for point_feature in in_point_features:
    try:
        # Construir el nombre único de la tabla de salida
        out_table_name = "Values_" + \
            os.path.splitext(os.path.basename(point_feature))[0]
        out_point_feature = os.path.join(out_dataset, out_table_name)

        # Ejecutar la herramienta ExtractValuesToPoints
        ExtractValuesToPoints(
            point_feature, in_raster, out_point_feature, interpolate_values, add_attributes)

        arcpy.AddMessage(
            "Se extrajeron valores correctamente para: {}".format(point_feature))
    except arcpy.ExecuteError:
        # Capturar y mostrar cualquier error
        arcpy.AddError(
            "Error al ejecutar ExtractValuesToPoints para: {}".format(point_feature))
        arcpy.AddError(arcpy.GetMessages())
    except Exception as e:
        # Capturar y mostrar cualquier otro error
        arcpy.AddError("Error inesperado para: {}".format(point_feature))
        arcpy.AddError(str(e))

# Mensaje de finalización
arcpy.AddMessage("Proceso finalizado")
