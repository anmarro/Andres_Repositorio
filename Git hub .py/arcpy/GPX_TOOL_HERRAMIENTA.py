import arcpy
import os

# Carpeta con los archivos GPX
input_workspace = arcpy.GetParameterAsText(0)
arcpy.AddMessage(
    "Carpeta con archivos GPX seleccionada: {}".format(input_workspace))


# Carpeta de salida para la geodatabase
output_workspace = arcpy.GetParameterAsText(1)
arcpy.AddMessage(
    "Carpeta de destino seleccionada: {}".format(output_workspace))

# Nombre de la geodatabase
gdb_name = arcpy.GetParameterAsText(2)
arcpy.AddMessage("Nombre de la GDB: {}".format(gdb_name))

# Nombre del Feature Dataset
feature_dataset_name = arcpy.GetParameterAsText(3)
arcpy.AddMessage("Nombre del dataset: {}".format(feature_dataset_name))

# Sistema de Referencia Espacial (SR)
sr = arcpy.GetParameter(4)
arcpy.AddMessage("Nombre del Sistema de referencia: {}".format(sr))

# Espacio de trabajo
arcpy.env.workspace = input_workspace
arcpy.env.overwriteOutput = True

# Verificar que todos los archivos en la carpeta tienen la extensión .gpx
for filename in arcpy.ListFiles():
    if not filename.lower().endswith('.gpx'):
        raise arcpy.ExecuteError(
            "La carpeta de entrada contiene archivos que no tienen la extensión .gpx")

# Crear la geodatabase en la carpeta de salida si no existe
gdb_path = os.path.join(output_workspace, "{}{}".format(gdb_name, ".gdb"))
if not arcpy.Exists(gdb_path):
    arcpy.CreateFileGDB_management(output_workspace, gdb_name)

# Crear el Feature Dataset si no existe
feature_dataset_path = os.path.join(gdb_path, feature_dataset_name)
if not arcpy.Exists(feature_dataset_path):
    arcpy.CreateFeatureDataset_management(gdb_path, feature_dataset_name)

# Listar archivos .gpx dentro del espacio de trabajo definido
listaGPX = arcpy.ListFiles("*.gpx")

for GPX in listaGPX:
    try:
        # Obtener el nombre base del archivo GPX
        nombre_base = os.path.splitext(GPX)[0]

        # Nombre del shapefile después de la validación
        nombre_shp = arcpy.ValidateTableName(nombre_base)

        # Ruta completa del archivo de salida shapefile
        shp = os.path.join(output_workspace, nombre_shp)

        # Convertir GPX a shapefile
        arcpy.conversion.GPXtoFeatures(GPX, shp)

        # Añadir el shapefile al Feature Dataset
        arcpy.conversion.FeatureClassToGeodatabase(shp, feature_dataset_path)

        arcpy.AddMessage(
            f"Archivo '{GPX}' convertido y añadido a la geodatabase.")

    except arcpy.ExecuteError as e:
        arcpy.AddError(f"Error al procesar el archivo '{GPX}': {str(e)}")
    except Exception as e:
        arcpy.AddError(
            f"Se ha producido un error inesperado al procesar el archivo '{GPX}': {str(e)}")

# Cambiar el espacio de trabajo al Feature Dataset
arcpy.env.workspace = feature_dataset_path

# Ahora convierto los feature classes de punto a línea
arcpy.AddMessage("Listando feature classes...")
fclass = arcpy.ListFeatureClasses("*", "POINT")
for fc in fclass:
    arcpy.AddMessage("Points to line...")
    fclass_linea = "{}_Linea".format(os.path.splitext(fc)[0])
    pointsToLine = arcpy.management.PointsToLine(os.path.join(
        feature_dataset_path, fc), os.path.join(feature_dataset_path, fclass_linea))

    # Elimino feature classes de puntos tras convertirlos a líneas
    arcpy.AddMessage("Eliminando feature classes de puntos...")
    arcpy.Delete_management(fc)


arcpy.AddMessage("Proceso finalizado.")
