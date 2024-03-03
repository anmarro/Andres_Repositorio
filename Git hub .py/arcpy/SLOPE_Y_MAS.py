import arcpy
from arcpy import env
from arcpy.sa import *
import os

# Espacio de trabajo y output
env.workspace = r""
arcpy.env.overwriteOutput = True

# MDE resultante, ahora le calculo mapa de pendientes y lo guardo
arcpy.AddMessage("Creando mapa de pendientes...")
pendiente = Slope(env.workspace, "DEGREE", "", method="PLANAR", z_unit="METER")
pendienteSave = r""
pendiente.save(pendienteSave)
print("Slope guardado")


# Ahora voy a reclasificar sus valores
arcpy.AddMessage("Reclasificando valores...")
reclas = Reclassify(pendienteSave, "Value", RemapRange(
    [[0, 25, 1], [25, 35, 2], [35, 45, 3], [45, 55, 4], [55, 90, 5]]))
reclasGuardado = r""
reclas.save(reclasGuardado)
print("Reclasificación hecha")


# Colores para cada reclasificación
arcpy.AddMessage("Definiendo colores para la reclasificación...")
customizedColormap = {"values": [1, 2, 3, 4, 5], "colors": [
    "#51BF00", "#FFAB4C", "#FE2300", "#FE7000", "#00FEDC"]}
coloreado = Colormap(reclasGuardado, colormap=customizedColormap)
pendientesColoreado = r""
coloreado.save(pendientesColoreado)
print("Coloreado")


"""
 [[0, 25, "Riesgo muy poco probable"], [25, 35, "Presencia de aludes cuando las condiciones son inestables"],
     [35, 45, "Mayor ocurrencia de avalanchas. Peligro máximo entre 38 y 39 grados"], [
         45, 55, "Frecuencia de purgas y pequeñas placas naturales"],
     [55, 90, "No se suelen acumular espesores. La nieve se purga con frecuencia"]]))
     """
