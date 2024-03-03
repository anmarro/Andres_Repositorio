import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r""

inRaster = r""
inFalseRaster = r""
sentencia = "VALUE <= 15 Or VALUE >=70 "
out_raster = r""
Pendiente_SetNull = SetNull(inRaster, inFalseRaster, sentencia)
Pendiente_SetNull.save(out_raster)

print("Proceso finalizado")
