import arcpy
import os
from arcpy import env
from arcpy.sa import *
import re

# Habilitar la sobrescritura de conjuntos de datos existentes
arcpy.env.overwriteOutput = True

# Definir el espacio de trabajo y la carpeta de salida
arcpy.env.workspace = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\RUTAS"
outputFolder = r"C:\PIRINEOS\GDB\PIRINEOS.gdb"

# Lista para almacenar todas las feature classes de puntos generadas
lista_fclasses_puntos = []
arcpy.AddMessage("Lista creada..")

# Definir el sistema de coordenadas
arcpy.AddMessage("Definiendo sistema de coordenadas...")
sistemaCoordenadasBase = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\RUTAS\ascension_por_corredor_estasen_petit_black_hasta_pico_aneto__Linea"
sistemaCoordenadas = arcpy.Describe(sistemaCoordenadasBase).spatialReference
arcpy.AddMessage("Iniciando iteración...")

# Generar puntos a lo largo de las líneas para cada archivo polilínea
for fclass in arcpy.ListFeatureClasses("*", "Polyline"):
    # Nombre del archivo de salida para los puntos
    output_base_name = "{}_points.shp".format(
        os.path.splitext(os.path.basename(fclass))[0])
    # Eliminar caracteres no válidos del nombre de archivo
    output_base_name = ''.join(
        c for c in output_base_name if c.isalnum() or c in ['_', '-'])
    # Ruta completa de salida para el archivo de puntos
    outputFclass = os.path.join(outputFolder, output_base_name)

    # Generar puntos a lo largo de las líneas
    arcpy.AddMessage(
        "Generando puntos a lo largo de las líneas para: {}".format(fclass))
    fclassPuntos = str(arcpy.management.GeneratePointsAlongLines(
        fclass, outputFclass, "DISTANCE", Distance="100 meters"))
    # Agregar la feature class de puntos a la lista
    lista_fclasses_puntos.append(fclassPuntos)

arcpy.AddMessage("Listando fclass de puntos...")

# Definir la ubicación del archivo de pendientes y la carpeta de salida
pendiente = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\Pendiente"
salida = r"C:\PIRINEOS\GDB\PIRINEOS.gdb"
puntosEntrada = lista_fclasses_puntos
arcpy.AddMessage("Iterando para extraer valores de pendientes a los puntos...")

# Iterar sobre las feature classes de puntos y extraer valores de pendiente
contador = 1
for fclassPuntos in puntosEntrada:
    # Nombre del archivo de salida con contador
    output_name = "{}_extracted_{}.shp".format(
        os.path.splitext(os.path.basename(fclassPuntos))[0], contador)

    # Imprimir el nombre del archivo de salida
    arcpy.AddMessage("Nombre del archivo de salida: {}".format(output_name))
    # Ruta completa de salida para el archivo de puntos
    outputPuntos = os.path.join(salida, output_name)

    # Extraer valores de pendiente a los puntos
    valoresPendiente_a_puntos = arcpy.sa.ExtractValuesToPoints(
        fclassPuntos, pendiente, outputPuntos, interpolate_values="NONE",
        add_attributes="VALUE_ONLY")

    # Incrementar el contador para la próxima iteración
    contador += 1

arcpy.AddMessage("Finalizado con éxito")
