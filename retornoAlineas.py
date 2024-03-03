import arcpy
import os

# ESPACIO DE TRABAJO
arcpy.env.workspace = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\VALORES_PENDIENTE"
arcpy.env.overwriteOutput = True

# Listo fclasses
arcpy.AddMessage("Listando feature classes...")
input_features = arcpy.ListFeatureClasses("*")

datasetName = "RUTAS_FULL"
gdb = r"C:\PIRINEOS\GDB\PIRINEOS.gdb"
spatialReference = arcpy.Describe(
    r"C:\PIRINEOS\GDB\PIRINEOS.gdb\Pendiente").spatialReference
arcpy.AddMessage("Creando dataset...")
rutasFull = arcpy.management.CreateFeatureDataset(
    gdb, datasetName, spatialReference)

sort_Field = "OBJECTID"
lineField = None
close_Line = "NO_CLOSE"
line_Construction_Method = "TWO_POINT"
attribute_Source = "BOTH_ENDS"
transfer_Fields = ["OBJECTID", "Name", "Descript", "Type", "Comment",
                   "Symbol", "DateTimeS", "Elevation", "DateTime", "RASTERVALU"]

arcpy.AddMessage("Iterando aplicando la herramienta")
for features in input_features:
    arcpy.AddMessage("Procesando: {}".format(features))
    try:
        # Reducir el nombre del archivo de salida a un máximo de 10 caracteres
        output_name = os.path.basename(features)[:25]
        outputFeatureClass = os.path.join(gdb, datasetName, output_name)
        arcpy.AddMessage("Aplicando la herramienta...")
        rutas_ok = arcpy.management.PointsToLine(
            features, outputFeatureClass, lineField, sort_Field, close_Line, line_Construction_Method,
            attribute_Source, transfer_Fields)
        arcpy.AddMessage("Herramienta aplicada correctamente.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(
            "Error al ejecutar PointsToLine para: {}".format(features))
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        # Capturar y mostrar cualquier otro error
        arcpy.AddError("Error inesperado para: {}".format(features))
        arcpy.AddError(str(e))

arcpy.AddMessage("Proceso finalizado")
