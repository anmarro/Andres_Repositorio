import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r"C:\PIRINEOS\GDB\PIRINEOS.gdb"

inRaster = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\Pendiente"
inFalseRaster = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\Pendiente"
sentencia = "VALUE <= 15 Or VALUE >=70 "
out_raster = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\Pendiente_SetNull"
Pendiente_SetNull = SetNull(inRaster, inFalseRaster, sentencia)
Pendiente_SetNull.save(out_raster)

print("Proceso finalizado")
