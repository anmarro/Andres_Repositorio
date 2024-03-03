import arcpy

# Establecer el espacio de trabajo
arcpy.env.workspace = r"espacio trabajo"

# Ruta de la capa de simbología .lyr
lyr_file = r"archivo .lyrx"

# Listar las feature classes en el espacio de trabajo
fclasses = arcpy.ListFeatureClasses("*")

# Iterar sobre cada feature class
for fclass in fclasses:
    arcpy.AddMessage("Feature Class: {}".format(fclass))

    # Verificar si la feature class tiene el campo "Peligro_Aludes"
    if arcpy.ListFields(fclass, "Peligro_Aludes"):
        arcpy.AddMessage("Aplicando simbología a la feature class...")

        # Aplicar simbología desde la capa de simbología .lyr
        arcpy.ApplySymbologyFromLayer_management(fclass, lyr_file)

        arcpy.AddMessage(
            "Simbología aplicada correctamente a la feature class: {}".format(fclass))
    else:
        arcpy.AddMessage(
            "No se encontró el campo 'Peligro_Aludes' en esta feature class")
