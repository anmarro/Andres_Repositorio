import arcpy
raster = r"C:\PIRINEOS\GDB\PIRINEOS.gdb\MDE"
desc = arcpy.Describe(raster)
proy = desc.spatialReference.name
print(proy)
