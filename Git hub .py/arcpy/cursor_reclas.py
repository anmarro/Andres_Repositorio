import arcpy
# espacio de trabajo
arcpy.env.workspace = r"ruta"
# listo fclasses
arcpy.AddMessage("Listando rutas...")
rutas = arcpy.ListFeatureClasses("*")
# Campos que contienen los valores de pendiente al inicio y al final de la entidad
campo_inicio_pendiente = "START_RASTERVALU"
campo_fin_pendiente = "END_RASTERVALU"

# Campo nuevo
campo_nuevo = "Peligro_Aludes"

# Definir la función para clasificar los valores


def clasificar_valor(inicio, fin):
    arcpy.AddMessage("Calculando promedios...")
    # Calcular el promedio de los valores de pendiente al inicio y al final
    valor_promedio = (inicio + fin) / 2
    if valor_promedio >= 0 and valor_promedio < 25:
        return "Avalanchas muy poco probables"
    elif valor_promedio >= 25 and valor_promedio < 35:
        return "Presencia de aludes cuando las condiciones son inestables"
    elif valor_promedio >= 35 and valor_promedio < 45:
        return "Mayor ocurrencia de aludes"
    elif valor_promedio >= 45 and valor_promedio < 55:
        return "Frecuencia de purgas y pequeñas placas naturales"
    else:
        return "La nieve se purga con frecuencia y no se suelen acumular grandes espesores"


# Procesar cada feature class
for ruta in rutas:
    # Iniciar la edición de la feature class
    try:
        # Agregar el campo nuevo si no existe
        if campo_nuevo not in [field.name for field in arcpy.ListFields(ruta)]:
            arcpy.AddField_management(
                ruta, campo_nuevo, "TEXT", field_length=100)

        arcpy.AddMessage("Aplicando update cursor...{}".format(ruta))
        with arcpy.da.UpdateCursor(ruta, [campo_inicio_pendiente, campo_fin_pendiente, campo_nuevo]) as cursor:
            for row in cursor:
                valor_inicio = row[0]
                valor_fin = row[1]
                clasificacion = clasificar_valor(valor_inicio, valor_fin)
                row[2] = clasificacion
                cursor.updateRow(row)
        arcpy.AddMessage(
            "La clasificación se ha aplicado correctamente a la feature class: {}".format(ruta))

    except arcpy.ExecuteError:
        # Capturar y mostrar cualquier error
        arcpy.AddError(
            "Error al ejecutar update cursor para la feature class: {}".format(ruta))
        arcpy.AddError(arcpy.GetMessages(2))
    except Exception as e:
        # Capturar y mostrar cualquier otro error
        arcpy.AddError(
            "Error inesperado al procesar la feature class: {}".format(ruta))
        arcpy.AddError(str(e))

arcpy.AddMessage("Proceso finalizado")
