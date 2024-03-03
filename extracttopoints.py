import arcpy
import os
from arcpy.sa import ExtractValuesToPoints

# Espacio de trabajo
arcpy.env.workspace = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\TRACKS_PUNTOS"
arcpy.env.overwriteOutput = True

# Lista de capas de puntos
arcpy.AddMessage("Listando feature classes...")
in_point_features = arcpy.ListFeatureClasses("*")
arcpy.AddMessage("Feature class listada: {}".format(in_point_features))

# Ruta del archivo raster de entrada
in_raster = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\Pendiente"

# Ruta del dataset de salida
out_dataset = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\VALORES_PENDIENTE"

# Configurar los parámetros de la herramienta
interpolate_values = "NONE"
add_attributes = "VALUE_ONLY"

# Iterar sobre las capas de puntos
arcpy.AddMessage("Iterando...")
for point_feature in in_point_features:
    try:
        arcpy.AddMessage("Construyendo ruta de salida...")
        # Construir la ruta de salida
        out_point_feature = os.path.join(
            out_dataset, os.path.basename(point_feature))

        # Ejecutar la herramienta ExtractValuesToPoints
        arcpy.AddMessage("Aplicando la herramienta...")
        ExtractValuesToPoints(
            point_feature, in_raster, out_point_feature, interpolate_values, add_attributes)

        arcpy.AddMessage(
            "Se han extraído valores correctamente para: {}".format(point_feature))
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
