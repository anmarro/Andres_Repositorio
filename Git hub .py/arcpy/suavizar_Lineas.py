import arcpy
import arcpy.cartography as CA

# Establecer el espacio de trabajo para las feature classes de entrada
arcpy.env.workspace = r""
arcpy.env.overwriteOutput = True

# Listar todas las feature classes en el espacio de trabajo
rutas = arcpy.ListFeatureClasses("*")

# Establecer la ruta de salida para las feature classes suavizadas
ruta_salida_suavizada = r""

# Iterar sobre cada feature class
for ruta in rutas:
    try:
        # Construir la ruta completa de la feature class de salida suavizada
        nombre_suavizado = "Suavizada_" + arcpy.ValidateTableName(ruta)
        ruta_completa_salida = ruta_salida_suavizada + "\\" + nombre_suavizado

        # Aplicar la herramienta de suavizado de líneas
        CA.SmoothLine(in_features=ruta, out_feature_class=ruta_completa_salida,
                      algorithm="BEZIER_INTERPOLATION", tolerance=0)

        # Imprimir mensaje de finalización
        arcpy.AddMessage("Suavizado completado para: {}".format(ruta))

    except arcpy.ExecuteError:
        # Capturar y mostrar cualquier error
        arcpy.AddError(
            "Error al ejecutar el suavizado de líneas para la feature class: {}".format(ruta))
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        # Capturar y mostrar cualquier otro error
        arcpy.AddError(
            "Error inesperado al procesar la feature class: {}".format(ruta))
        arcpy.AddError(str(e))

arcpy.AddMessage("Proceso finalizado")
