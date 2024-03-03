import arcpy
from arcpy import env
from arcpy.sa import *

# Establecer la carpeta de trabajo
env.workspace = r""

# Listar todos los rasters en la carpeta
arcpy.AddMessage("Listando rasters...")
MDT = arcpy.ListRasters()

# Definir la ruta y nombre de la geodatabase de salida
output_gdb = r""

# Definir el nombre del mosaico
mosaic_name = "Mosaico_MDT"

# Fusionar todos los rasters en un nuevo raster dentro de la geodatabase de salida
arcpy.AddMessage("Mosaico a new raster iniciando...")
arcpy.management.MosaicToNewRaster(
    ';'.join(MDT), output_gdb, "Mosaico_MDT", pixel_type="32_BIT_FLOAT", number_of_bands=1)

print("Proceso finalizado")
